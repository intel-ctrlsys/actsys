"""Add device history in favor of logical deletion

Revision ID: 8d64bce23c6b
Revises: e4d4e95ae481
Create Date: 2017-03-16 12:52:57.852420

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSTZRANGE, JSONB
from sqlalchemy import false as false_just_for_sqlalchemy
import textwrap

# revision identifiers, used by Alembic.
revision = '8d64bce23c6b'
down_revision = 'e4d4e95ae481'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Get this to use the op/sa functions better.
    op.execute("""
ALTER TABLE device ADD COLUMN sys_period tstzrange not null default tstzrange(current_timestamp, null);

UPDATE device set sys_period = tstzrange(current_timestamp, null);
CREATE TABLE device_history(LIKE device INCLUDING DEFAULTS);

CREATE OR REPLACE FUNCTION device_history_version() returns trigger as $$
BEGIN
  if (TG_OP = 'UPDATE') then
    INSERT INTO public.device_history
    (device_id, device_type, properties, hostname, ip_address, mac_address, profile_name, sys_period)
    VALUES
    (OLD.device_id, OLD.device_type, OLD.properties, OLD.hostname, OLD.ip_address, OLD.mac_address, OLD.profile_name,
    tstzrange(lower(OLD.sys_period), current_timestamp));

    NEW.sys_period = tstzrange(current_timestamp, null);

    return new;
  elsif (TG_OP = 'DELETE') then
    INSERT INTO public.device_history
    (device_id, device_type, properties, hostname, ip_address, mac_address, profile_name, sys_period)
    VALUES
    (OLD.device_id, OLD.device_type, OLD.properties, OLD.hostname, OLD.ip_address, OLD.mac_address, OLD.profile_name,
    tstzrange(lower(OLD.sys_period), current_timestamp));

    return old;
  end if;
end;
$$ LANGUAGE plpgsql;

CREATE TRIGGER device_history_upd
  before update or delete on device
  for each row execute procedure device_history_version();""")

    op.execute("DELETE FROM public.device where deleted = True;")
    op.drop_column('device', 'deleted')
    op.drop_column('device_history', 'deleted')
    op.execute(
        "CREATE VIEW device_with_history as SELECT * FROM public.device UNION ALL SELECT * FROM public.device_history;")
    op.execute("DROP FUNCTION public.delete_device_logical(character varying);")

    op.execute("ALTER FUNCTION public.delete_device_fatal(character varying) RENAME TO delete_device;")
    op.execute(textwrap.dedent("""
            CREATE OR REPLACE FUNCTION public.delete_device(p_device_name character varying)
            RETURNS SETOF change_result AS
            $BODY$
            DECLARE num_rows integer;
            DECLARE v_device_id integer;
            BEGIN
                IF (p_device_name is not null) THEN
                    v_device_id := public.get_device_id(p_device_name);
                    DELETE FROM public.device WHERE device_id=v_device_id;

                GET DIAGNOSTICS num_rows = ROW_COUNT;
                RETURN QUERY SELECT num_rows, v_device_id;
                END IF;
            RETURN QUERY SELECT 0, 0;
            END;

            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;
        """))

    op.drop_constraint("log_process", "log")
    # op.create_foreign_key("fk_log_device_history", "log", "device_history", ["device_id"], ["device_id"])
    # Add sys_period to type
    op.execute(textwrap.dedent("""
        ALTER TYPE type_device_details ADD ATTRIBUTE sys_period tstzrange;
    """))
    # Remove 'where device.deleted` check
    op.execute(textwrap.dedent("""
           CREATE OR REPLACE FUNCTION public.get_device_details(p_device_name character varying)
           RETURNS SETOF type_device_details AS
           $BODY$

           DECLARE
           result_device_details type_device_details;
           v_device_id integer;

           BEGIN
               -- Get the device details
               IF (p_device_name is null) THEN
               -- return all of them...
                   RETURN QUERY SELECT device_id, device_type, device.properties,
                       hostname, ip_address, mac_address, device.profile_name, profile.properties, sys_period
                   FROM device
                   LEFT JOIN profile ON device.profile_name = profile.profile_name
                   ORDER BY device.device_id;
               ELSE
               -- Get the device ID
                   v_device_id := public.get_device_id(p_device_name);
               -- Just get the one
                   RETURN QUERY SELECT device_id, device_type, device.properties,
                       hostname, ip_address, mac_address, device.profile_name, profile.properties, sys_period
                   FROM device
                   LEFT JOIN profile ON device.profile_name = profile.profile_name
                   WHERE device_id = v_device_id
                   ORDER BY device.device_id;
               END IF;
               RETURN;
           END


           $BODY$
               LANGUAGE plpgsql VOLATILE
               COST 100;
       """))
    # Remove device.deleted check
    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.get_profile_devices(p_profile_name character varying)
        RETURNS SETOF integer AS
        $BODY$

        DECLARE
        result_device_details type_device_details;

        BEGIN
            -- Get the device details
            RETURN QUERY SELECT device_id
            FROM public.device
            WHERE profile_name = p_profile_name
            ORDER BY device_id;
        END


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;

    """))
    # Get history function
    op.execute(textwrap.dedent("""
           CREATE OR REPLACE FUNCTION public.get_device_history(p_device_name character varying)
           RETURNS SETOF type_device_details AS
           $BODY$

           DECLARE
           result_device_details type_device_details;
           v_device_id integer;

           BEGIN
               -- Get the device details
               IF (p_device_name is null) THEN
               -- return all of them...
                   RETURN QUERY SELECT device_id, device_type, properties,
                       hostname, ip_address, mac_address, profile_name, cast(null AS JSONB), sys_period
                   FROM device_with_history
                   ORDER BY sys_period;
               ELSE
                   -- Just get things that match
                   RETURN QUERY SELECT device_id, device_type, properties,
                       hostname, ip_address, mac_address, profile_name, cast(null AS JSONB), sys_period
                   FROM device_history
                   WHERE device_id = cast_to_int(p_device_name, 0)
                      or hostname = p_device_name
                      or ip_address = p_device_name
                   ORDER BY sys_period;
               END IF;
               RETURN;
           END


           $BODY$
               LANGUAGE plpgsql VOLATILE
               COST 100;
       """))


def downgrade():
    op.execute("""DROP TRIGGER device_history_upd ON public.device;""")
    op.execute("""DROP FUNCTION public.device_history_version();""")
    op.execute("""DROP FUNCTION public.get_device_history(character varying);""")

    op.execute("DROP VIEW device_with_history;")
    op.drop_table('device_history')
    op.drop_column("device", "sys_period")
    op.add_column("device",
                  sa.Column('deleted', sa.BOOLEAN(), server_default=false_just_for_sqlalchemy(), nullable=False))

    op.execute(textwrap.dedent("""
          CREATE OR REPLACE FUNCTION public.delete_device_logical(p_device_name character varying)
          RETURNS SETOF change_result AS
          $BODY$
          DECLARE
          num_rows integer;
          v_device_id integer;
          BEGIN
              IF (p_device_name IS NULL) THEN
                  RETURN QUERY SELECT 0,0;
              END IF;
              v_device_id := public.get_device_id(p_device_name);
              UPDATE public.device SET deleted = true
              WHERE device.device_id = v_device_id;

              GET DIAGNOSTICS num_rows = ROW_COUNT;
              RETURN QUERY SELECT num_rows, v_device_id;
          END;

          $BODY$
              LANGUAGE plpgsql VOLATILE
              COST 100;
      """))

    op.execute("ALTER FUNCTION public.delete_device(character varying) RENAME TO delete_device_fatal;")
    op.execute(textwrap.dedent("""
            CREATE OR REPLACE FUNCTION public.delete_device_fatal(p_device_name character varying)
            RETURNS SETOF change_result AS
            $BODY$
            DECLARE num_rows integer;
            DECLARE v_device_id integer;
            BEGIN
                IF (p_device_name is not null) THEN
                    v_device_id := public.get_device_id(p_device_name);
                    DELETE FROM public.log WHERE device_id=v_device_id;
                    DELETE FROM public.device WHERE device_id=v_device_id;

                GET DIAGNOSTICS num_rows = ROW_COUNT;
                RETURN QUERY SELECT num_rows, v_device_id;
                END IF;
            RETURN QUERY SELECT 0, 0;
            END;

            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;
        """))

    # op.drop_constraint("fk_log_device_history", "log")
    op.create_foreign_key("log_process", "log", "device", ["device_id"], ["device_id"])

    op.execute(textwrap.dedent("""
            CREATE OR REPLACE FUNCTION public.get_device_details(p_device_name character varying)
            RETURNS SETOF type_device_details AS
            $BODY$

            DECLARE
            result_device_details type_device_details;
            v_device_id integer;

            BEGIN
                -- Get the device details
                IF (p_device_name is null) THEN
                -- return all of them...
                    RETURN QUERY SELECT device_id, device_type, device.properties,
                        hostname, ip_address, mac_address, device.profile_name, profile.properties
                    FROM device
                    LEFT JOIN profile ON device.profile_name = profile.profile_name
                    WHERE device.deleted = false
                    ORDER BY device.device_id;
                ELSE
                -- Get the device ID
                    v_device_id := public.get_device_id(p_device_name);
                -- Just get the one
                    RETURN QUERY SELECT device_id, device_type, device.properties,
                        hostname, ip_address, mac_address, device.profile_name, profile.properties
                    FROM device
                    LEFT JOIN profile ON device.profile_name = profile.profile_name
                    WHERE device_id = v_device_id AND device.deleted = false
                    ORDER BY device.device_id;
                END IF;
                RETURN;
            END


            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;
        """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.get_profile_devices(p_profile_name character varying)
        RETURNS SETOF integer AS
        $BODY$

        DECLARE
        result_device_details type_device_details;

        BEGIN
            -- Get the device details
            RETURN QUERY SELECT device_id
            FROM public.device
            WHERE profile_name = p_profile_name and deleted is False
            ORDER BY device_id;
        END


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;

    """))

    # Remove sys_period to type
    op.execute(textwrap.dedent("""
            ALTER TYPE type_device_details DROP ATTRIBUTE IF EXISTS sys_period;
        """))

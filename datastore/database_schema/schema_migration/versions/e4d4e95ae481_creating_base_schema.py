#
# Copyright (c) 2017 Intel Corporation. All rights reserved
#

"""creating base schema

Revision ID: e4d4e95ae481
Revises: 
Create Date: 2017-02-16 16:32:08.305724

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import false as false_just_for_sqlalchemy
from sqlalchemy.sql import func
import textwrap

# revision identifiers, used by Alembic.
revision = 'e4d4e95ae481'
down_revision = None
branch_labels = None
depends_on = None


def creating_functions():
    op.execute(textwrap.dedent("""
       CREATE TYPE change_result AS (affected_rows integer, device_id integer);
    """))

    op.execute(textwrap.dedent("""
        CREATE TYPE type_device_details AS (device_id integer, device_type character varying,
        properties jsonb, hostname character varying, ip_address character varying,
        mac_address character varying, profile_name character varying, profile_properties jsonb);
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.add_log(p_process character varying, p_timestamp timestamp with time zone,
        p_level integer, p_device_name character varying, p_message text)
        RETURNS integer AS
        $BODY$
        DECLARE num_rows integer;
        DECLARE m_device_id integer;
        BEGIN
            m_device_id := null;
            IF (p_device_name is not null) THEN
                m_device_id := public.get_device_id(p_device_name);
            END IF;

            EXECUTE 'INSERT INTO public.log (message, level' ||
                CASE WHEN p_process IS NULL THEN '' ELSE ', process' END ||
                CASE WHEN p_timestamp IS NULL THEN '' ELSE ', timestamp' END ||
                CASE WHEN m_device_id IS NULL THEN '' ELSE ', device_id' END ||')
            VALUES (' || quote_literal(p_message) ||', ' || p_level ||
                CASE WHEN p_process IS NULL THEN '' ELSE ', ' || quote_literal(p_process) END ||
                CASE WHEN p_timestamp IS NULL THEN '' ELSE ', ' || quote_literal(p_timestamp) END ||
                CASE WHEN m_device_id IS NULL THEN '' ELSE ', ' || m_device_id END ||');';

        GET DIAGNOSTICS num_rows = ROW_COUNT;
        RETURN num_rows;
        END;

        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.cast_to_int(character varying, integer)
        RETURNS integer AS
        $BODY$
        BEGIN
            RETURN cast($1 as integer);
            EXCEPTION when invalid_text_representation THEN
            RETURN $2;
        END;

        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.delete_configuration_value(p_key character varying)
        RETURNS integer AS
        $BODY$
        DECLARE num_rows integer;
        BEGIN
            DELETE FROM configuration WHERE key = p_key;

        GET DIAGNOSTICS num_rows = ROW_COUNT;
        RETURN num_rows;
        END;

        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

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

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.delete_profile(p_profile_name character varying)
        RETURNS integer AS
        $BODY$
        DECLARE num_rows integer;
        BEGIN
            DELETE FROM public.profile
            WHERE profile_name = p_profile_name;

            GET DIAGNOSTICS num_rows = ROW_COUNT;
            RETURN num_rows;
        END;

        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.get_configuration_value(p_key character varying)
        RETURNS character varying AS
        $BODY$

        DECLARE passed character varying;
        BEGIN
            SELECT value INTO passed
            FROM configuration
            WHERE key = p_key;
            RETURN passed;
        END;


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

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
        CREATE OR REPLACE FUNCTION public.get_device_id(p_device_name character varying)
        RETURNS integer AS
        $BODY$

        DECLARE
        v_device_id integer;
        BEGIN
            v_device_id := NULL;
            -- Get the device id based on the device_name
            IF (p_device_name IS NOT NULL) THEN
            -- check for matching device_id
                SELECT device_id INTO v_device_id
                FROM public.device where device_id = cast_to_int(p_device_name, 0)
                ORDER BY device_id ASC;

                -- check for matching hostnames
                IF (v_device_id IS NULL) THEN
                    SELECT device_id INTO v_device_id
                    FROM public.device where hostname = p_device_name
                    ORDER BY device_id ASC;
                END IF;

                -- Check for matching ip_addresses
                IF (v_device_id IS NULL) THEN
                    SELECT device_id INTO v_device_id
                    FROM public.device where ip_address = p_device_name
                    ORDER BY device_id ASC;
                END IF;
            END IF;
            RETURN v_device_id;
        END


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.get_log(IN p_device_name character varying, IN p_limit integer)
        RETURNS TABLE(process character varying, "timestamp" timestamp with time zone, level integer, device_id integer,
        message text) AS
        $BODY$

        BEGIN

            IF (p_device_name is null) THEN
                RETURN QUERY SELECT l.process, l.timestamp, l.level, l.device_id, l.message FROM public.log AS l
                    ORDER BY l.timestamp DESC LIMIT p_limit;
            ELSE
                RETURN QUERY SELECT process, "timestamp", level, device_id, message FROM public.log
                    WHERE device_id = p_device_name ORDER BY l.timestamp DESC LIMIT p_limit;
            END IF;

        END;


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    # TODO this one might need device_name translated into device_id
    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.get_log_timeslice(
        IN p_device_name character varying,
        IN p_limit integer,
        IN p_time_begin timestamp with time zone,
        IN p_time_end timestamp with time zone)
        RETURNS TABLE(process character varying, "timestamp" timestamp with time zone, level integer, device_id integer, message text) AS
        $BODY$

        BEGIN

            IF (p_device_name is null) THEN
                RETURN QUERY SELECT l.process, l.timestamp, l.level, l.device_id, l.message
                FROM public.log AS l
                WHERE l.timestamp BETWEEN p_time_begin AND p_time_end
                ORDER BY l.timestamp DESC LIMIT p_limit;
            ELSE
                RETURN QUERY SELECT process, "timestamp", level, device_id, message
                FROM public.log
                WHERE l.device_id = p_device_name AND l.timestamp BETWEEN p_time_being AND p_time_end
                ORDER BY l.timestamp DESC LIMIT p_limit;
            END IF;

        END;


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.get_profile(IN p_profile_name character varying)
        RETURNS TABLE(profile_ame character varying, properties jsonb) AS
        $BODY$

        DECLARE passed character varying;
        BEGIN

            IF (p_profile_name is null) THEN
                RETURN QUERY SELECT p.profile_name, p.properties FROM public.profile AS p;
            ELSE
                RETURN QUERY SELECT p.profile_name, p.properties FROM public.profile AS p WHERE profile_name = p_profile_name;
            END IF;

        END;


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

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.upsert_configuration_value(p_key character varying, p_value character varying)
        RETURNS integer AS
        $BODY$

        DECLARE num_rows integer;
        BEGIN
            INSERT INTO public.configuration AS cfg (key, value)
            VALUES (p_key, p_value)
            ON CONFLICT (key) DO UPDATE
            SET value = p_value
            WHERE cfg.key = p_key;

            GET DIAGNOSTICS num_rows = ROW_COUNT;
            RETURN num_rows;
        END;

        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.upsert_device(p_device_id integer, p_device_type character varying,
            p_hostname character varying, p_ip_address character varying, p_mac_address character varying,
            p_hardware_type character varying, p_profile_name character varying, p_properties jsonb)
        RETURNS SETOF change_result AS
        $BODY$
        DECLARE num_rows integer;
        BEGIN
            IF (p_device_id is null) THEN
                INSERT INTO public.device(device_type, properties, hostname, ip_address, mac_address, profile_name)
                VALUES(p_device_type, p_properties, p_hostname, p_ip_address, p_mac_address, p_profile_name)
                RETURNING public.device.device_id into p_device_id;
            ELSE
        -- We are either specifying our own id, or updating
                INSERT INTO public.device(device_id, device_type, properties, hostname, ip_address, mac_address, profile_name)
                VALUES(p_device_id, p_device_type, p_properties, p_hostname, p_ip_address, p_mac_address, p_profile_name)
                ON CONFLICT ON CONSTRAINT device_pkey DO UPDATE
                SET
                    device_type = COALESCE(p_device_type, device.device_type),
                    properties = COALESCE(p_properties, device.properties),
                    hostname = COALESCE(p_hostname, device.hostname),
                    ip_address = COALESCE(p_ip_address, device.ip_address),
                    mac_address = COALESCE(p_mac_address, device.mac_address),
                    profile_name = COALESCE(p_profile_name, device.profile_name)
                WHERE device.device_id = p_device_id;
            END IF;
        GET DIAGNOSTICS num_rows = ROW_COUNT;
        RETURN QUERY SELECT num_rows, p_device_id;
        END;

        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))

    op.execute(textwrap.dedent("""
        CREATE OR REPLACE FUNCTION public.upsert_profile(p_profile_name character varying, p_properties jsonb)
        RETURNS integer AS
        $BODY$

        DECLARE num_rows integer;
        BEGIN
            INSERT INTO public.profile AS pro (profile_name, properties)
            VALUES (p_profile_name, p_properties)
            ON CONFLICT (profile_name) DO UPDATE
            SET
                properties = p_properties
            WHERE pro.profile_name = p_profile_name;
            GET DIAGNOSTICS num_rows = ROW_COUNT;
            RETURN num_rows;
        END;


        $BODY$
            LANGUAGE plpgsql VOLATILE
            COST 100;
    """))


def drop_functions():
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.add_log(character varying, timestamp with time zone, integer, character varying, text);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.cast_to_int(character varying, integer);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.delete_configuration_value(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.delete_device_fatal(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.delete_device_logical(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.delete_profile(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_configuration_value(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_device_details(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_device_id(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_log(character varying, integer);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_log_timeslice(character varying, integer, timestamp with time zone, timestamp with time zone);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_profile(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.get_profile_devices(character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.upsert_configuration_value(character varying, character varying);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.upsert_device(integer, character varying, character varying, character varying, character varying, character varying, character varying, jsonb);
    """))
    op.execute(textwrap.dedent("""
        DROP FUNCTION public.upsert_profile(character varying, jsonb);
    """))
    op.execute(textwrap.dedent("""
    DROP TYPE IF EXISTS type_device_details;
    """))

    op.execute(textwrap.dedent("""
    DROP TYPE IF EXISTS change_result;
    """))


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('profile',
                    sa.Column('profile_name', sa.String(length=128), nullable=False),
                    sa.Column('properties', JSONB(), nullable=False),
                    sa.PrimaryKeyConstraint('profile_name', name=op.f('profile_pkey'))
                    )

    op.create_table('configuration',
                    sa.Column('key', sa.String(length=128), nullable=False),
                    sa.Column('value', sa.String(length=1024), nullable=False),
                    sa.PrimaryKeyConstraint('key', name=op.f('configuration_pkey'))
                    )

    op.create_table('device',
                    sa.Column('device_id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('device_type', sa.String(length=64), nullable=False),
                    sa.Column('properties', JSONB(), nullable=True),
                    sa.Column('hostname', sa.String(length=256), nullable=True),
                    sa.Column('ip_address', sa.String(length=64), nullable=True),
                    sa.Column('mac_address', sa.String(length=64), nullable=True),
                    sa.Column('profile_name', sa.String(length=128), nullable=True),
                    sa.Column('deleted', sa.BOOLEAN(), server_default=false_just_for_sqlalchemy(), nullable=False),
                    sa.PrimaryKeyConstraint('device_id', name=op.f('device_pkey')),
                    sa.ForeignKeyConstraint(['profile_name'], ['profile.profile_name'], name='device_profile',
                                            match='SIMPLE', ondelete='NO ACTION', onupdate='NO ACTION')
                    )

    op.create_table('log',
                    sa.Column('process', sa.String(length=128), nullable=True),
                    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
                    sa.Column('level', sa.Integer(), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('message', sa.Text(), nullable=False),
                    sa.ForeignKeyConstraint(['device_id'], ['device.device_id'], name='log_process',
                                            match='SIMPLE', ondelete='NO ACTION', onupdate='NO ACTION'),
                    sa.CheckConstraint('level = ANY (ARRAY[0, 10, 15, 20, 30, 40, 50])', name=op.f('valid_log_levels'))
                    )

    creating_functions()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    drop_functions()
    op.drop_table('log')
    op.drop_table('device')
    op.drop_table('profile')
    op.drop_table('configuration')
    # ### end Alembic commands ###

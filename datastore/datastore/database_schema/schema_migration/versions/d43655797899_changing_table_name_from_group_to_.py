"""Changing table name from 'group' to 'device_group'

Revision ID: d43655797899
Revises: 38f3c80e9932
Create Date: 2017-08-24 15:17:10.671537

"""
import textwrap
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd43655797899'
down_revision = '38f3c80e9932'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(textwrap.dedent("""ALTER TABLE public.group RENAME TO device_group;"""))
    op.execute(textwrap.dedent("""
            CREATE OR REPLACE FUNCTION public.upsert_group(p_group_name character varying, p_device_list character varying)
            RETURNS integer AS
            $BODY$
            DECLARE num_rows integer;
            BEGIN
                INSERT INTO public.device_group AS gro (group_name, device_list)
                VALUES (p_group_name, p_device_list)
                ON CONFLICT (group_name) DO UPDATE
                SET
                    device_list = p_device_list
                WHERE gro.group_name = p_group_name;
                GET DIAGNOSTICS num_rows = ROW_COUNT;
                RETURN num_rows;
            END;
            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;"""))


def downgrade():
    op.execute(textwrap.dedent("""ALTER TABLE device_group RENAME TO "group";"""))
    op.execute(textwrap.dedent("""
            CREATE OR REPLACE FUNCTION public.upsert_group(p_group_name character varying, p_device_list character varying)
            RETURNS integer AS
            $BODY$
            DECLARE num_rows integer;
            BEGIN
                INSERT INTO public.group AS gro (group_name, device_list)
                VALUES (p_group_name, p_device_list)
                ON CONFLICT (group_name) DO UPDATE
                SET
                    device_list = p_device_list
                WHERE gro.group_name = p_group_name;
                GET DIAGNOSTICS num_rows = ROW_COUNT;
                RETURN num_rows;
            END;
            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;"""))

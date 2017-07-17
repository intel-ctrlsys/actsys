"""empty message

Revision ID: 38f3c80e9932
Revises: 8d64bce23c6b
Create Date: 2017-06-08 10:18:53.432112

"""
import textwrap
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38f3c80e9932'
down_revision = '8d64bce23c6b'
branch_labels = None
depends_on = None


def upgrade():
    """
    Upgrade to add groups.
    :return:
    """
    op.create_table('group',
                    sa.Column('group_name', sa.String(length=128), nullable=False),
                    sa.Column('device_list', sa.String(length=1024), nullable=False),
                    sa.PrimaryKeyConstraint('group_name', name=op.f('group_pkey'))
                    )

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


def downgrade():
    """
    Remove the add group items
    :return:
    """
    op.execute(textwrap.dedent("""DROP FUNCTION public.upsert_group(character varying, character varying);"""))
    op.drop_table('group')

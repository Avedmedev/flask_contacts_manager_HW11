"""Initial migration2

Revision ID: f46c964087f6
Revises: 7c9836dd2c16
Create Date: 2022-12-12 15:27:12.339250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f46c964087f6"
down_revision = "7c9836dd2c16"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "owners",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("login", sa.String(length=120), nullable=False),
        sa.Column("hash", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "persons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("work_place", sa.String(length=120), nullable=True),
        sa.Column("post_name", sa.String(length=120), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["owners.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "emails",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone_number", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=120), nullable=True),
        sa.Column("person_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["person_id"], ["persons.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "phones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone_number", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=120), nullable=True),
        sa.Column("person_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["person_id"], ["persons.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("phones")
    op.drop_table("emails")
    op.drop_table("persons")
    op.drop_table("owners")
    # ### end Alembic commands ###

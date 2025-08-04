"""remove_unused_tables_config_performance_podcast

Revision ID: bb99bb79a360
Revises: 45cf4bc63dfc
Create Date: 2025-08-04 11:08:12.273034

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bb99bb79a360"
down_revision: Union[str, Sequence[str], None] = "45cf4bc63dfc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop unused tables
    op.drop_table("podcast")
    op.drop_table("performance_tracking")
    op.drop_table("config")


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate config table
    op.create_table(
        "config",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("parameter", sa.VARCHAR(length=100), nullable=True),
        sa.Column("indicator", sa.VARCHAR(length=100), nullable=True),
        sa.Column("val_min", sa.DECIMAL(precision=15, scale=6), nullable=True),
        sa.Column("val_max", sa.DECIMAL(precision=15, scale=6), nullable=True),
        sa.Column("step", sa.DECIMAL(precision=15, scale=6), nullable=True),
        sa.Column("current", sa.DECIMAL(precision=15, scale=6), nullable=True),
        sa.Column("new_champion", sa.DECIMAL(precision=15, scale=6), nullable=True),
        sa.Column("test", sa.DECIMAL(precision=15, scale=6), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("parameter"),
    )

    # Recreate performance_tracking table
    op.create_table(
        "performance_tracking",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("performance", sa.VARCHAR(length=100), nullable=False),
        sa.Column("current", sa.DECIMAL(precision=15, scale=6), nullable=False),
        sa.Column("new", sa.DECIMAL(precision=15, scale=6), nullable=False),
        sa.Column("limit", sa.VARCHAR(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Recreate podcast table
    op.create_table(
        "podcast",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("date", sa.TIMESTAMP(), nullable=False),
        sa.Column("conclusion", sa.TEXT(), nullable=False),
        sa.Column("meteo_date", sa.TIMESTAMP(), nullable=False),
        sa.Column("meteo_conclusion", sa.TEXT(), nullable=False),
        sa.Column("press_date", sa.TIMESTAMP(), nullable=False),
        sa.Column("press_author", sa.VARCHAR(length=100), nullable=False),
        sa.Column("press_text", sa.TEXT(), nullable=False),
        sa.Column("position", sa.VARCHAR(length=100), nullable=False),
        sa.Column("dialogue", sa.TEXT(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("date"),
    )

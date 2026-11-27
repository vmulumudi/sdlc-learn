"""create notes table with pgvector embedding

Revision ID: 0001
Revises:
"""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # On Azure Postgres Flexible Server this only works after VECTOR is allow-listed
    # in the server parameter `azure.extensions` (we set that in Bicep, Phase 7).
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("embedding", Vector(64), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    # HNSW = approximate nearest-neighbour index; vector_cosine_ops matches the <=> operator.
    op.execute("CREATE INDEX ix_notes_embedding ON notes USING hnsw (embedding vector_cosine_ops)")


def downgrade() -> None:
    op.drop_table("notes")

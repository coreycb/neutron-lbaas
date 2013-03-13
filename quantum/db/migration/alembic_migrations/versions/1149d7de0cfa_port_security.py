# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 OpenStack LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""inital port security

Revision ID: 1149d7de0cfa
Revises: 1b693c095aa3
Create Date: 2013-01-22 14:05:20.696502

"""

# revision identifiers, used by Alembic.
revision = '1149d7de0cfa'
down_revision = '1b693c095aa3'

# Change to ['*'] if this migration applies to all plugins

migration_for_plugins = [
    'quantum.plugins.nicira.nicira_nvp_plugin.QuantumPlugin.NvpPluginV2'
]

from alembic import op
import sqlalchemy as sa

from quantum.db import migration


def upgrade(active_plugin=None, options=None):
    if not migration.should_run(active_plugin, migration_for_plugins):
        return

    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('networksecuritybindings',
                    sa.Column('network_id', sa.String(length=36),
                    nullable=False),
                    sa.Column('port_security_enabled', sa.Boolean(),
                    nullable=False),
                    sa.ForeignKeyConstraint(['network_id'], ['networks.id'],
                    ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('network_id'))
    op.create_table('portsecuritybindings',
                    sa.Column('port_id', sa.String(length=36),
                    nullable=False),
                    sa.Column('port_security_enabled', sa.Boolean(),
                    nullable=False),
                    sa.ForeignKeyConstraint(['port_id'], ['ports.id'],
                    ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('port_id'))
    ### end Alembic commands ###

    # Copy network and port ids over to network|port(securitybindings) table
    # and set port_security_enabled to false as ip address pairs were not
    # configured in NVP originally.
    op.execute("INSERT INTO networksecuritybindings SELECT id as "
               "network_id, False as port_security_enabled from networks")
    op.execute("INSERT INTO portsecuritybindings SELECT id as port_id, "
               "False as port_security_enabled from ports")


def downgrade(active_plugin=None, options=None):
    if not migration.should_run(active_plugin, migration_for_plugins):
        return

    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portsecuritybindings')
    op.drop_table('networksecuritybindings')
    ### end Alembic commands ###

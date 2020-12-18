# region Licensing
# SPDX-FileCopyrightText: 2020 Luka Žaja <luka.zaja@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

""" refind-btrfs - Generate rEFInd manual boot stanzas from Btrfs snapshots
Copyright (C) 2020  Luka Žaja

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# endregion

from typing import List, Type

from injector import Binder, Module, SingletonScope, multiprovider, provider
from transitions.core import State
from watchdog.events import FileSystemEventHandler

from refind_btrfs.boot.file_refind_config_provider import FileRefindConfigProvider
from refind_btrfs.common import CheckableObserver
from refind_btrfs.common.abc import (
    BaseDeviceCommandFactory,
    BaseLoggerFactory,
    BasePackageConfigProvider,
    BasePersistenceProvider,
    BaseRefindConfigProvider,
    BaseRunner,
    BaseSubvolumeCommandFactory,
)
from refind_btrfs.common.enums import States
from refind_btrfs.console import CLIRunner
from refind_btrfs.service import SnapshotEventHandler, SnapshotObserver, WatchdogRunner
from refind_btrfs.state_management import Model, RefindBtrfsMachine
from refind_btrfs.state_management.states import (
    InitBlockDevicesState,
    InitBtrfsMetadataState,
    InitRefindConfigState,
    PrepareSnapshotsState,
    ProcessChangesState,
)
from refind_btrfs.system import (
    BtrfsUtilSubvolumeCommandFactory,
    SystemDeviceCommandFactory,
)

from .file_package_config_provider import FilePackageConfigProvider
from .logger_factories import StreamLoggerFactory, SystemdLoggerFactory
from .shelve_persistence_provider import ShelvePersistenceProvider


class CommonModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(BaseDeviceCommandFactory, to=SystemDeviceCommandFactory)
        binder.bind(BaseSubvolumeCommandFactory, to=BtrfsUtilSubvolumeCommandFactory)

        # singletons
        binder.bind(
            BasePackageConfigProvider,
            to=FilePackageConfigProvider,
            scope=SingletonScope,
        )
        binder.bind(
            BaseRefindConfigProvider, to=FileRefindConfigProvider, scope=SingletonScope
        )
        binder.bind(
            BasePersistenceProvider, to=ShelvePersistenceProvider, scope=SingletonScope
        )

    @provider
    def provide_machine(
        self,
        logger_factory: BaseLoggerFactory,
        model: Model,
        states: List[Type[State]],
    ) -> RefindBtrfsMachine:
        return RefindBtrfsMachine(logger_factory, model, states)

    @provider
    def provide_model(
        self,
        logger_factory: BaseLoggerFactory,
        package_config_provider: BasePackageConfigProvider,
        persistence_provider: BasePersistenceProvider,
    ) -> Model:
        return Model(logger_factory, package_config_provider, persistence_provider)

    @multiprovider
    def provide_states(
        self,
        device_command_factory: BaseDeviceCommandFactory,
        subvolume_command_factory: BaseSubvolumeCommandFactory,
        refind_config_provider: BaseRefindConfigProvider,
        persistence_provider: BasePersistenceProvider,
    ) -> List[Type[State]]:
        return [
            State(name=States.INITIAL.value),
            InitBlockDevicesState(device_command_factory),
            InitBtrfsMetadataState(subvolume_command_factory),
            InitRefindConfigState(refind_config_provider),
            PrepareSnapshotsState(persistence_provider),
            ProcessChangesState(
                device_command_factory,
                subvolume_command_factory,
                refind_config_provider,
                persistence_provider,
            ),
            State(name=States.FINAL.value),
        ]


class WatchdogModule(CommonModule):
    def configure(self, binder: Binder) -> None:
        super().configure(binder)

        binder.bind(BaseRunner, to=WatchdogRunner)
        binder.bind(CheckableObserver, to=SnapshotObserver)
        binder.bind(FileSystemEventHandler, to=SnapshotEventHandler)
        binder.bind(BaseLoggerFactory, to=SystemdLoggerFactory)


class CLIModule(CommonModule):
    def configure(self, binder: Binder) -> None:
        super().configure(binder)

        binder.bind(BaseRunner, to=CLIRunner)
        binder.bind(BaseLoggerFactory, to=StreamLoggerFactory)

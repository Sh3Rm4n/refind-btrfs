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

from pathlib import Path
from uuid import UUID


ROOT_UID = 0

EX_NOT_OK = 1
EX_ARGPARSE_ERROR = 2
EX_CTRL_C_INTERRUPT = 130

NOTIFICATION_READY = "READY=1"
NOTIFICATION_STOPPING = "STOPPING=1"
NOTIFICATION_STATUS = "STATUS={0}"
NOTIFICATION_ERRNO = "ERRNO={0}"

MESSAGE_CTRL_C_INTERRUPT = "Ctrl+C interrupt detected, exiting..."
MESSAGE_UNEXPECTED_ERROR = "An unexpected error happened, exiting..."

WATCH_TIMEOUT = 1
BACKGROUND_MODE_PID_NAME = "refind-btrfs-watchdog"

MTAB_PT_TYPE = "mtab"
FSTAB_PT_TYPE = "fstab"

ESP_PART_CODE = 0xEF
ESP_PART_UUID = UUID(hex="c12a7328-f81f-11d2-ba4b-00a0c93ec93b")

ESP_FS_TYPE = "vfat"
BTRFS_TYPE = "btrfs"

SNAPSHOT_COUNT_INFINITY = "inf"
SNAPSHOTS_ROOT_DIR_PERMISSIONS = 0o750

COMMENT_PATTERN = r"^\s*#.*"
INCLUDE_OPTION_PATTERN = r"^include .+$"
PARAMETERIZED_OPTION_PREFIX_PATTERN = r"^\S+="
DIR_SEPARATOR_PATTERN = r"\\|/"

ROOTFLAGS_PREFIX = "rootflags="
INITRD_PREFIX = "initrd="
SUBVOL_OPTION = "subvol"
SUBVOLID_OPTION = "subvolid"

PARAMETERIZED_OPTION_SEPARATOR = "="
BOOT_OPTION_SEPARATOR = " "
COLUMN_SEPARATOR = ","

SPACE = " "
TAB = SPACE * 4
DOUBLE_QUOTE = '"'
BACKSLASH = "\\"
FORWARD_SLASH = "/"
NEWLINE = "\n"
EMPTY_STR = ""
EMPTY_HEX_UUID = "00000000-0000-0000-0000-000000000000"
EMPTY_UUID = UUID(hex=EMPTY_HEX_UUID)

CONFIG_FILE_EXTENSION = ".conf"

DEFAULT_PATH = Path()
ROOT_DIR = Path("/")
BOOT_DIR = Path("boot")
ETC_DIR = Path("etc")
VAR_DIR = Path("var")
LIB_DIR = Path("lib")
SNAPSHOT_STANZAS_CONFIG_DIR = Path("btrfs-snapshot-stanzas")
PACKAGE_DIR = Path("refind-btrfs")

FSTAB_FILE = ETC_DIR / "fstab"
PACKAGE_CONFIG_FILE = ROOT_DIR / ETC_DIR / "refind-btrfs.conf"
DB_FILE = ROOT_DIR / VAR_DIR / LIB_DIR / PACKAGE_DIR / "local_db"

# Copyright 2019-2021 Cambridge Quantum Computing
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from shutil import copyfile
import platform

from conans import ConanFile, tools


def libfile(name):
    sysname = platform.system()
    if sysname == "Linux":
        return "lib" + name + ".so"
    elif sysname == "Darwin":
        return "lib" + name + ".dylib"
    elif sysname == "Windows":
        return name + ".dll"
    else:
        return None


class TketTestsTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    keep_imports = True

    def imports(self):
        self.copy("*", src="@bindirs", dst="bin")
        self.copy("*", src="@libdirs", dst="lib")

    def test(self):
        if not tools.cross_building(self):
            for name in ["tket"]:
                fname = libfile(name)
                copyfile(
                    os.path.join(self.install_folder, "lib", fname),
                    os.path.join("bin", fname),
                )
            cmd_extra = "" if platform.system() == "Linux" else ' "~[latex]"'
            os.chdir("bin")
            self.run(os.path.join(os.curdir, "test_tket" + cmd_extra))
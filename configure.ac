# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
define([VERSION_MAJOR], [1])
define([VERSION_MINOR], [9])
define([VERSION_FIX], [4])
define([VERSION_NUMBER], VERSION_MAJOR[.]VERSION_MINOR[.]VERSION_FIX)
define([VERSION_SUFFIX], [_master])

AC_INIT([python-amcrest], VERSION_NUMBER[]VERSION_SUFFIX, [tchello.mello@gmail.com])
PACKAGE_NAME="python-amcrest"
PACKAGE_RPM_VERSION="VERSION_NUMBER"
PACKAGE_RPM_RELEASE="0"
AM_INIT_AUTOMAKE([-Wall -Werror foreign -Wno-portability tar-pax])

AC_SUBST([PACKAGE_RPM_VERSION])
AC_SUBST([PACKAGE_RPM_RELEASE])
AC_SUBST([COMMIT])
AC_SUBST([SHORT_COMMIT])

AC_PROG_INSTALL
AC_PROG_SED
AC_PROG_MAKE_SET
AC_PROG_MKDIR_P
AC_PROG_LN_S

AM_CONDITIONAL(BUILD_PYTHON3, false)

AC_PATH_PROG([PYTHON3], [python3], [no])
[if test "$PYTHON3" == "no"]
[then]
    AM_PATH_PYTHON([2])
    AC_SUBST([amcrestpythonlibdir], ["\$(pythondir)/amcrest"])
[else]
    AC_SUBST([PYTHON3_PREFIX], ['${prefix}'])
    AC_SUBST([PYTHON3_EXEC_PREFIX], ['${exec_prefix}'])

    PYTHON3_DIR=`$PYTHON3 -c "import distutils.sysconfig; \
        print(distutils.sysconfig.get_python_lib(0,0,prefix='$PYTHON3_PREFIX'))"`
    PYTHON3_EXECDIR=`$PYTHON3 -c "import distutils.sysconfig; \
        print(distutils.sysconfig.get_python_lib(1,0,prefix='$PYTHON3_EXEC_PREFIX'))"`

    AC_SUBST(PYTHON3_CFLAGS)
    AC_SUBST(PYTHON3_LIBS)
    AC_SUBST(python3dir, $PYTHON3_DIR)
    AC_SUBST(py3execdir, $PYTHON3_EXECDIR)
    AC_SUBST([amcrestpythonlibdir], ["\$(python3dir)/amcrest"])
[fi]

# Python tools
AC_ARG_VAR([PYFLAKES], [flake8 utility])
AC_CHECK_PROGS([PYFLAKES], [flake8])

AC_CONFIG_FILES([
		Makefile
		src/amcrest/Makefile
		man/Makefile
		cli/Makefile
		tui/Makefile
		setup.py
		python-amcrest.spec])
AC_OUTPUT

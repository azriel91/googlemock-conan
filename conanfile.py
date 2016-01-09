from conans import *

class GoogleMockConan(ConanFile):
    name = 'googlemock'
    version = '1.7.0'
    settings = ['os', 'compiler', 'build_type', 'arch']
    generators = ['cmake']
    url = 'https://github.com/azriel91/googlemock-conan.git'
    options = {
        'BUILD_SHARED_LIBS':       ['ON', 'OFF'], # Build shared libraries (DLLs).
        'gmock_build_tests':       ['ON', 'OFF'], # Build all of Google Mock's own tests.
        'gtest_force_shared_crt':  ['ON', 'OFF'], # Use shared (DLL) run-time lib even when Google Test is built as static lib.
        'gtest_build_tests':       ['ON', 'OFF'], # Build all of gtest's own tests.
        'gtest_build_samples':     ['ON', 'OFF'], # Build gtest's sample programs.
        'gtest_disable_pthreads':  ['ON', 'OFF'], # Disable uses of pthreads in gtest.

        # Set this to 0 if your project already uses a tuple library, and GTest should use that library
        # Set this to 1 if GTest should use its own tuple library
        'GTEST_USE_OWN_TR1_TUPLE': [None, '0', '1'],

        # Set this to 0 if GTest should not use tuple at all. All tuple features will be disabled
        'GTEST_HAS_TR1_TUPLE':     [None, '0'],

        # If GTest incorrectly detects whether or not the pthread library exists on your system, you can force it
        # by setting this option value to:
        #   1 - if pthread does actually exist
        #   0 - if pthread does not actually exist
        'GTEST_HAS_PTHREAD':       [None, '0', '1']
    }
    default_options = ('BUILD_SHARED_LIBS=OFF',
                       'gmock_build_tests=OFF',
                       'gtest_force_shared_crt=OFF',
                       'gtest_build_tests=OFF',
                       'gtest_build_samples=OFF',
                       'gtest_disable_pthreads=OFF',
                       'GTEST_USE_OWN_TR1_TUPLE=None',
                       'GTEST_HAS_TR1_TUPLE=None',
                       'GTEST_HAS_PTHREAD=None')

    gtest_version = version
    gtest_dir = 'gtest'
    build_dir = 'build'

    def source(self):
        googlemock_url = 'https://github.com/google/googlemock.git'
        release_tag = 'release-{version}'.format(version=self.version)
        self.run("git clone {url} --branch {branch} --depth 1".format(url=googlemock_url, branch=release_tag))

        # Google Mock needs to compile with Google Test sources alongside its source
        google_test_url = 'https://github.com/google/googletest.git'
        release_tag = 'release-{version}'.format(version=self.gtest_version)
        self.run("git clone {url} {gtest_dir} --branch {branch} --depth 1".format(url=google_test_url,
                                                                                  gtest_dir=self.gtest_dir,
                                                                                  branch=release_tag))

    def requirements(self):
        # We require googletest so that others requiring googlemock don't have to
        self.requires("googletest/{gtest_version}@azriel91/stable-1".format(gtest_version=self.gtest_version))

    def config(self):
        # googlemock is compiled with googletest sources, so if linking to googletest, we must also link to a version
        # compiled with the same options
        pass_through_options = ('gtest_force_shared_crt',
                                'gtest_build_tests',
                                'gtest_build_samples',
                                'gtest_disable_pthreads',
                                'GTEST_USE_OWN_TR1_TUPLE',
                                'GTEST_HAS_TR1_TUPLE',
                                'GTEST_HAS_PTHREAD')
        googletest_options = self.options['googletest']
        for opt in pass_through_options:
            setattr(googletest_options, opt, getattr(self.options, opt))

    def build(self):
        option_defines = ' '.join("-D%s=%s" % (opt, val) for (opt, val) in self.options.iteritems() if val is not None)
        self.run("cmake {src_dir} -B{build_dir} {defines}".format(src_dir=self.name,
                                                                  build_dir=self.build_dir,
                                                                  defines=option_defines))
        self.run("cmake --build {build_dir}".format(build_dir=self.build_dir))

    def package(self):
        self.copy('*', dst='cmake', src="{src_dir}/cmake".format(src_dir=self.name), keep_path=True)
        self.copy('*', dst='include', src="{src_dir}/include".format(src_dir=self.name), keep_path=True)
        self.copy('CMakeLists.txt', dst='.', src=self.name, keep_path=True)

        # Meta files
        self.copy('CHANGES', dst='.', src=self.name, keep_path=True)
        self.copy('CONTRIBUTORS', dst='.', src=self.name, keep_path=True)
        self.copy('LICENSE', dst='.', src=self.name, keep_path=True)
        self.copy('README', dst='.', src=self.name, keep_path=True)

        # Built artifacts
        if self.options['BUILD_SHARED_LIBS'] == 'ON':
            self.copy('libgmock.so', dst='lib', src=self.build_dir, keep_path=False)
            self.copy('libgmock_main.so', dst='lib', src=self.build_dir, keep_path=False)
        else:
            self.copy('libgmock.a', dst='lib', src=self.build_dir, keep_path=False)
            self.copy('libgmock_main.a', dst='lib', src=self.build_dir, keep_path=False)

        # Commented code intentionally left here
        # ======================================
        # IDE sample files
        # self.copy('*', dst='make', src="{src_dir}/make".format(src_dir=self.name))
        # self.copy('*', dst='msvc', src="{src_dir}/msvc".format(src_dir=self.name))

        # Autoconf/Automake
        # self.copy('configure.ac', dst='configure.ac', src=self.name)
        # self.copy('Makefile.am', dst='Makefile.am', src=self.name)

        # Files not used by downstream
        # self.copy('*', dst='build-aux', src="{src_dir}/build-aux".format(src_dir=self.name))
        # self.copy('*', dst='scripts', src="{src_dir}/scripts".format(src_dir=self.name))
        # self.copy('*', dst='src', src="{src_dir}/src".format(src_dir=self.name))
        # self.copy('*', dst='test', src="{src_dir}/test".format(src_dir=self.name))

    def package_info(self):
        self.cpp_info.libs.append('gmock')

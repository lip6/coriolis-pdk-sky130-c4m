
project(
  'coriolis-pdk-sky130-c4m',
   version:  '2024.10.15',
   meson_version: '>= 1.2.0',
)

py       = import( 'python' ).find_installation( pure:false )
py_deps  = dependency( 'python3', required: true )
pdks_dir = py.get_install_dir() / 'pdks' / 'sky130_c4m'

python_file = ['pdkmaster/__init__.py'
              ]
core2chip_files = [ 'pdkmaster/core2chip/__init__.py'
                  , 'pdkmaster/core2chip/sky130.py']


py.install_sources( files(     python_file), subdir:'pdks/sky130_c4m' )
py.install_sources( files(  core2chip_files), subdir:'pdks/sky130_c4m/core2chip') 
install_subdir( 'pdkmaster/C4M.Sky130/' , install_dir:pdks_dir )



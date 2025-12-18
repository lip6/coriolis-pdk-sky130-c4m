
from pathlib import Path
from coriolis.designflow.task    import ShellEnv
__all__ = [ 'setup','pdkMasterTop' ]
pdkMasterTop = None
def setup ():
    from coriolis                     import Cfg 
    from coriolis                     import Viewer
    from coriolis                     import CRL 
    from coriolis.designflow.iverilog import Iverilog
    from coriolis.designflow.klayout  import Klayout
   #from coriolis.designflow.drc      import DRC
    from coriolis.designflow.lvx      import Lvx
    from coriolis.designflow.x2y      import x2y

    from coriolis.designflow.tasyagle import TasYagle
    from coriolis.helpers             import setNdaTopDir, overlay, l, u, n
    from coriolis.designflow.yosys    import Yosys
    pdkMasterTop = Path( __file__ ).parent /'C4M.Sky130'



    if isinstance(pdkMasterTop,str):
        pdkMasterTop = Path( pdkMasterTop )
    ndaDirectory = None
    if pdkMasterTop:
        ndaDirectory = pdkMasterTop / 'libs.tech' / 'coriolis' / 'techno'
    elif not ndaDirectory:
        hostname = socket.gethostname()
        if hostname.startswith('lepka'):
            ndaDirectory = Path( '/dsk/l1/jpc/crypted/soc/techno' )
            if not ndaDirectory.is_dir():
                print ('[ERROR] You forgot to mount the NDA encrypted directory, stupid!')
        else:
            ndaDirectory = Path( '/users/soft/techno/techno' )
        pdkMasterTop = ndaDirectory
    setNdaTopDir( ndaDirectory.as_posix() )
    if not pdkMasterTop.is_dir():
        print( '[ERROR] technos.setupSky130_c4m(): pdkMasterTop directory do *not* exists:' )
        print( '        "{}"'.format(pdkMasterTop.as_posix()) )
    from node130.sky130 import techno, StdCellLib #, LibreSOCIO
    from coriolis.designflow.technos import Where
    techno.setup()
    StdCellLib.setup()

    #LibreSOCIO.setup()

    cellsTop = pdkMasterTop / 'libs.ref'
    liberty  = cellsTop / 'StdCellLib' / 'liberty' / 'StdCellLib_nom.lib'
    
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.misc.catchCore           = False
        cfg.misc.minTraceLevel       = 12300
        cfg.misc.maxTraceLevel       = 12400
        cfg.misc.info                = False
        cfg.misc.paranoid            = False
        cfg.misc.bug                 = False
        cfg.misc.logMode             = True
        cfg.misc.verboseLevel1       = False
        cfg.misc.verboseLevel2       = False
        cfg.viewer.pixelThreshold    = 5
        cfg.etesian.graphics         = 2
        cfg.anabatic.topRoutingLayer = 'm4'
        cfg.katana.eventsLimit       = 4000000
        af  = CRL.AllianceFramework.get()
        lg5 = af.getRoutingGauge( 'StdCellLib' ).getLayerGauge( 5 ) 
        lg5.setType( CRL.RoutingLayerGauge.PowerSupply )
        env = af.getEnvironment()
        env.setCLOCK( '^sys_clk$|^ck|^jtag_tck$' )

    Yosys.setLiberty( liberty )
    spiceCells  =pdkMasterTop / 'libs.ref' / 'StdCellLib' / 'spice'
    stdCellLibVlog = pdkMasterTop / 'libs.ref' / 'StdCellLib' /'verilog'/ 'stdcell.v'
    ngspiceTech    = pdkMasterTop    /'libs.tech'/'ngspice'
    lypFile        =pdkMasterTop / 'libs.tech' / 'klayout' / 'tech' / 'C4M.Sky130'/ 'sky130.lyp'
    kdrcRulesC4M   = pdkMasterTop / 'libs.tech' / 'klayout' / 'tech' / 'C4M.Sky130' / 'drc' / 'DRC.lydrc'

    shellEnv = ShellEnv( 'sky130_c4m GF Alliance Environment' )
    shellEnv[ 'MBK_CATA_LIB' ] = shellEnv[ 'MBK_CATA_LIB' ] + ':' + spiceCells.as_posix()
    shellEnv.export()
    Klayout.setLypFile( lypFile )
    #DRC.setDrcRules( kdrcRulesC4M, DRC.C4M )
    #TODO incompleted DRC rules
    #DRC.setDrcRules( kdrcRulesMax, DRC.Maximal )
    #TODO sealring and filler
    Iverilog.setStdCellLib( stdCellLibVlog )
    TasYagle.flags         = TasYagle.Transistor
    TasYagle.SpiceType     = 'hspice'
    TasYagle.SpiceTrModel  = [ 'C4M.Sky130_logic_tt_model.spice']
    TasYagle.MBK_CATA_LIB  = (pdkMasterTop/'libs.ref'/'StdCellLib' / 'spice').as_posix() + ':' + (ngspiceTech).as_posix()
    Lvx.MBK_CATA_LIB  = TasYagle.MBK_CATA_LIB
    x2y.MBK_CATA_LIB  = TasYagle.MBK_CATA_LIB
    TasYagle.MBK_SPI_MODEL = ''
    TasYagle.Temperature   = 25.0
    TasYagle.VddSupply     = 1.8 
    TasYagle.VddName       = 'vdd'
    TasYagle.VssName       = 'vss'
    TasYagle.ClockName     = 'clk'





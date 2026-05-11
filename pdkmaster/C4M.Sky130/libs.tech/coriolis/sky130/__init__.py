
from pathlib import Path
from coriolis.designflow.task    import ShellEnv
from coriolis.designflow.technos import Where
from coriolis.technos.common.dft import DftStdCells

__all__ = [ 'setup', 'pdkMasterTop' ]


pdkMasterTop = None


def setup ():
    global pdkMasterTop

    from coriolis                     import Cfg 
    from coriolis                     import Viewer
    from coriolis                     import CRL 
    from coriolis.designflow.iverilog import Iverilog
    from coriolis.designflow.klayout  import Klayout, DRC
    from coriolis.designflow.lvx      import Lvx
    from coriolis.designflow.x2y      import x2y
    from coriolis.designflow.tasyagle import TasYagle
    from coriolis.helpers             import setNdaTopDir, overlay, l, u, n
    from coriolis.designflow.yosys    import Yosys
    from .techno                      import setup as techno_setup 
    from .StdCellLib                  import setup as StdCellLib_setup
    from .StdCell5V0Lib               import setup as StdCell5V0Lib_setup
    from .MacroLib                    import setup as macro_setup
    #from .IOLib                       import setup as io_setup

    pdkMasterTop = Path( __file__ ).parent
    techDir      = pdkMasterTop / 'libs.tech'
    stdCellDir   = pdkMasterTop / 'libs.ref' / 'StdCellLib'

    techno_setup()
    StdCellLib_setup()
    macro_setup()
    #io_setup()

    liberty  = stdCellDir / 'liberty' / 'StdCellLib_nom.lib'
    
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
    spiceCells     = stdCellDir / 'spice'
    stdCellLibVlog = stdCellDir /'verilog'/ 'stdcell.v'
    ngspiceTechDir = techDir / 'ngspice'
    lypFile        = techDir / 'klayout' / 'tech' / 'C4M.Sky130' / 'sky130.lyp'
    kdrcRulesC4M   = techDir / 'klayout' / 'tech' / 'C4M.Sky130' / 'drc' / 'DRC.lydrc'

    shellEnv = ShellEnv( 'SkyWater 130A Alliance Environment' )
    shellEnv[ 'MBK_CATA_LIB' ] = shellEnv[ 'MBK_CATA_LIB' ] + ':' + spiceCells.as_posix()
    shellEnv.export()
    Klayout.setLypFile( lypFile )
    DRC.setDrcRules( kdrcRulesC4M )
    Iverilog.setStdCellLib( stdCellLibVlog )
    TasYagle.flags         = TasYagle.Transistor
    TasYagle.SpiceType     = 'hspice'
    TasYagle.SpiceTrModel  = [ 'C4M.Sky130_logic_tt_model.spice' ]
    TasYagle.MBK_CATA_LIB  = (stdCellDir / 'spice').as_posix() + ':' + ngspiceTechDir.as_posix()
    Lvx.MBK_CATA_LIB       = TasYagle.MBK_CATA_LIB
    x2y.MBK_CATA_LIB       = TasYagle.MBK_CATA_LIB
    ShellEnv.MBK_SPI_MODEL = techDir / 'coriolis' / 'sky130' / 'spimodel.cfg'
    TasYagle.MBK_SPI_MODEL = ShellEnv.MBK_SPI_MODEL
    TasYagle.Temperature   = 25.0
    TasYagle.VddSupply     = 1.8 
    TasYagle.VddName       = 'vdd'
    TasYagle.VssName       = 'vss'
    TasYagle.ClockName     = 'clk'
    
def getDftStdCells():
   dft = DftStdCells()

   # -------- Supported flip-flops (no native scan FF available) --------
   dft.dff_names = [
       "dff_x1",
       "dffnr_x1",
   ]

   # -------- No FF → Scan FF mapping (fallback to mux-based scan FF creation) --------
   dft.ff_to_scanff = {
       # empty → will trigger create_scan_ff()
   }

   # -------- Fallback cells (used to build scan FFs) --------
   dft.mux_name = "mux2_x1"
   dft.buf_name = "buf_x1"

   # -------- Functional FF pin mapping --------
   dft.ff_pins = {
       "d": "i",
       "q": "q",
   }

   # -------- Scan control pins (must always be defined) --------
   dft.scan_pins = {
       "si": "SI",
       "se": "SE",
   }

   # -------- Mux pin mapping --------
   dft.mux_pins = {
       "i0": "i0",
       "i1": "i1",
       "sel": "cmd",
       "out": "q",
   }

   # -------- Buffer pin mapping --------
   dft.buf_pins = {
       "i": "i",
       "z": "q",
   }

   # -------- Placement orientations --------
   dft.mux_orientation = "ID"
   dft.ff_orientation  = "ID"

   return dft



  

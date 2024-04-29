from converter.animation.AnimationSource import AnimationSource
from converter.slal.SLALGroupSchema import SLALGroupSchema
from converter.slsb.SLSBGroupSchema import SLSBGroupchema
from converter.fnis.FNISAnimationStage import FNISAnimationStage
from converter.Arguments import Arguments
import os

class SLALPack:

    def __init__(self, dir):
        self.name = dir
        self.working_dir = os.path.join(Arguments.parent_dir, dir)
        self.slal_dir = self.working_dir + "\\SLAnims\\json"
        self.anim_source_dir = self.working_dir + "\\SLAnims\\source"
        
        self.out_dir = Arguments.parent_dir + "\\conversion\\" + dir

        self.actor_dir = self.working_dir + '\\meshes\\actors'

        self.FNIS_data: dict[str, FNISAnimationStage] = dict()

        self.groups: dict[str, PackGroup] = dict()

        print(f"{self.toString()} | Found")
        
    
    def validate(self):
        if not os.path.exists(self.slal_dir):
            return False
        #if not os.path.exists(self.anim_source_dir): ## TODO: Should this check be here? Or can this sometimes not exist?
        #    return False
        if not os.path.exists(self.actor_dir):
            return False
        return True
    
    ##NOTE: Yes, the source text can be missing at times (komotor, 3j, and some other have it missing iirc; also the manual conversions for zaz/ddng too)

    def setup(self):
        os.makedirs(self.out_dir + '/SKSE/Sexlab/Registry/Source')

    def toString(self):
        return f"[SLALPack] {self.name}"

    
class PackGroup:
    slal_json: SLALGroupSchema
    slsb_json: SLSBGroupchema
    animation_source: AnimationSource
    
    def __init__(self, name):
        self.name = name
        self.slal_json_filename: str = name + ".json"
        self.slsb_json_filename: str = name + ".slsb.json"

        self.animation_source = None
        self.slal_json = None
        self.slsb_json = None


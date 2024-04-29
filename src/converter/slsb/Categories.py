from converter.Keywords import Keywords
from converter.slsb.SLSBGroupSchema import PositionSchema, SexSchema
from converter.slsb.Tags import Tags

class SubCategories:
    unconscious = False   # necro stuff
    gore = False          # something gets chopped off
    amputee = False       # missing one/more limbs
    ryona = False         # dilebrately hurting sub
    humiliation = False   # includes punishments too
    forced = False        # rape and general non-consensual
    asphyxiation = False  # involving choking sub
    spanking = False      # you guessed it
    dominant = False       # consensual bdsm

    def submissive(self) -> bool:
        return any(getattr(self, attr) for attr in dir(self) if isinstance(getattr(self, attr), bool))
    
    def get_true(self) -> list[str]:
        return [attr for attr in dir(self) if  isinstance(getattr(self, attr), bool) and getattr(self, attr)]

class Categories:
    submissive = False
    sub_categories: SubCategories = SubCategories()
    maledom = False
    femdom = False
    maybe_femdom = False
    dead = False
    leadin = False
    restraint = ''
    furniture = ''
    straight = False
    gay = False
    lesbian = False
    futa = False
    scaling = False
    anim_object_found = False

    female_count = 0
    male_count = 0

    has_strap_on = []
    has_sos_value = []
    has_schlong = []
    has_add_cum = []
    has_forward = []
    has_side = []
    has_up = []
    has_rotate = []

    def __init__(self, tags: list[str], scene_name: str, anim_dir_name: str):
        self._set_categories(tags)
        self._set_sub_categories(tags, scene_name, anim_dir_name)


    def _set_categories(self, tags: list[str]) -> None:
        self.submissive = Tags.if_keywords_in_tags(tags, Keywords.sub) or Tags.if_keywords_in_tags(tags, Keywords.restraints)
        self.maledom = Tags.if_keywords_in_tags(tags, Keywords.sub) or Tags.if_keywords_in_tags(tags, Keywords.restraints)

        try:
            self.restraint = Tags.get_keyword_in_tags(tags, Keywords.restraints)
        except StopIteration:
            self.restraint = None

        self.maybe_femdom = Tags.if_keywords_in_tags(tags, Keywords.femdom)
        self.dead = Tags.if_keywords_in_tags(tags, Keywords.dead)

        self.leadin = 'leadin' in tags
        self.scaling = 'scaling' in tags
            
        if self.submissive and self.maybe_femdom:
            self.maledom = False
            self.femdom = True

        self.futa = Tags.if_keywords_in_tags(tags, Keywords.futa)

    def _set_sub_categories(self, tags: list[str], scene_name: str, anim_dir_name: str) -> None:     
        self.sub_categories.asphyxiation = 'asphyxiation' in tags
        self.sub_categories.spanking = 'spanking' in tags
        self.sub_categories.gore = 'gore' in tags

        self.sub_categories.dominant = Tags.if_in_tags(tags, scene_name, anim_dir_name, Keywords.dominant)
        self.sub_categories.ryona = Tags.if_in_tags(tags, scene_name, anim_dir_name, ['nya', 'psycheslavepunishment'])
        self.sub_categories.unconscious = Tags.if_in_tags(tags, scene_name, anim_dir_name, Keywords.unconscious)
        self.sub_categories.amputee = Tags.if_in_tags(tags, scene_name, anim_dir_name, ['amputee'])
        self.sub_categories.humiliation = Tags.if_in_tags(tags, scene_name, anim_dir_name, ['humiliation', 'punishment'])
        self.sub_categories.forced = Tags.if_in_tags(tags, scene_name, anim_dir_name, Keywords.forced)
        ## Note: for forced, I removed the check for 'Keywords.uses_only_agg_tag' because is there ever going to be a use of the 'aggressive' tag without it being forced?

        if self.submissive is not True:
            self.submissive = self.sub_categories.submissive()

        tags + self.sub_categories.get_true()

    def check_anim_object_found(self, positions: list[PositionSchema]):
        self.anim_object_found = any(pos['anim_obj'] != "" and "cum" not in pos['anim_obj'].lower() for pos in positions)

    def update_orientation(self, sex: SexSchema):
       
        if sex['male'] is True:
            self.male_count += 1
        if sex['female'] is True:
            self.female_count += 1

        self.straight = self.male_count > 0 and self.female_count > 0
        self.gay = self.male_count > 0 and self.female_count == 0
        self.lesbian = self.female_count > 0 and self.male_count == 0
"""Editable ship-specific annotation, measured on the ORIGINAL gray PNG.

Coordinates are pixel centers, x right, y down. Mirroring below only expands
unshaded geometry annotations; illumination is evaluated once in canonical space.
These are inferred artistic regions and pivot suggestions, not original CAD data.
"""
from .core import *

def point(p, scale=1):
    x,y=p
    return ((16 + (1065-y+.5)*333/1066-.5)*scale,
            (16 + (x+.5)*640/2047-.5)*scale)

def inverse(p):
    u,v=p
    return ((v-16+.5)*2047/640-.5, 1065-((u-16+.5)*1066/333-.5))

def definition():
    regions=[]
    def poly(name,mat,pts,pair=False,height=1):
        regions.append({'name':name,'material':mat,'polygon_source':pts,'height_semantic':height})
        if pair:
            regions.append({'name':name+'_opposite','material':mat,'polygon_source':[[x,1066-y] for x,y in pts], 'height_semantic':height})
    poly('forward_shoulder','paint',[[100,490],[500,285],[657,282],[664,326],[575,475],[398,491]],True,2)
    poly('shoulder_lit_plate','pale',[[180,468],[516,299],[577,329],[411,480]],True,2.2)
    poly('forward_center_spine','pale',[[50,512],[180,495],[568,494],[614,475],[634,488],[634,579],[614,591],[568,574],[180,571],[50,550]],False,2)
    poly('lateral_deck','paint',[[670,325],[735,281],[969,281],[968,317],[1292,318],[1350,440],[665,440]],True,1.3)
    poly('lateral_plate','pale',[[711,341],[852,328],[1058,332],[1100,362],[1080,406],[690,406]],True,1.8)
    poly('main_deck','pale',[[634,464],[1181,464],[1265,492],[1281,573],[1180,603],[634,603]],False,2)
    poly('center_raised_deck','framing',[[691,510],[888,504],[921,520],[921,548],[888,563],[691,556]],False,2.6)
    poly('aft_inner_bed','machinery',[[1320,243],[1610,248],[1680,407],[1565,449],[1371,417]],True,.5)
    poly('aft_outer_frame','paint',[[1098,146],[1210,106],[1659,116],[1692,199],[1750,317],[1800,354],[1940,415],[1915,468],[1710,407],[1650,317],[1595,181],[1227,181],[1162,227],[1124,217]],True,1.5)
    poly('aft_cross_brace','framing',[[1270,223],[1310,227],[1402,428],[1378,452],[1347,450],[1320,362]],True,2.1)
    poly('stern_assembly_base','paint',[[1682,409],[1799,372],[1950,418],[2014,482],[2030,534],[2014,588],[1950,650],[1799,694],[1682,657]],False,1.6)
    poly('aft_center_spear','pale',[[1210,530],[1253,502],[1330,501],[1590,519],[1615,535],[1590,553],[1330,566],[1253,565]],False,3)
    poly('forward_pod','paint',[[610,204],[655,190],[893,190],[925,205],[932,231],[905,247],[650,248],[610,233]],True,1.7)
    poly('aft_pod','paint',[[1353,39],[1381,21],[1602,19],[1680,25],[1709,49],[1709,71],[1661,88],[1381,85],[1353,69]],True,1.7)
    # Explicit repeated machinery units: placed at observed pairs, not scattered texture.
    for x in (755,814,1130,1184):
        poly(f'lateral_service_box_{x}','machinery',[[x-16,337],[x+18,337],[x+18,394],[x-16,394]],True,2.3)
    circles=[{'name':'rear_circular_assembly','source_center':[1766,533],'source_radius':84,'material':'framing'},
             {'name':'forward_circular_assembly','source_center':[561,533],'source_radius':29,'material':'framing'}]
    landmarks=[('bow',(2,533),'bow'),('left_forward_shoulder',(510,776),'structure'),('right_forward_shoulder',(510,290),'structure'),
        ('forward_weapon_pivot',(170,533),'weapon'),('center_deck',(820,533),'structure'),
        ('rear_ring',(1766,533),'circle'),('small_engine_left',(924,845),'engine'),('small_engine_right',(924,221),'engine'),
        ('large_engine_left',(1710,1012),'engine'),('large_engine_right',(1710,54),'engine'),
        ('aft_weapon_left',(1870,615),'weapon'),('aft_weapon_right',(1870,451),'weapon'),
        ('aft_outer_weapon_left',(1170,866),'weapon'),('aft_outer_weapon_right',(1170,198),'weapon')]
    # Source alpha checks use genuine empty spaces, not dark machinery.
    openings=[{'name':'aft_opening_left','source':[1565,745]}, {'name':'aft_opening_right','source':[1565,321]},
              {'name':'small_aft_gap_left','source':[1280,804]}, {'name':'small_aft_gap_right','source':[1280,262]}]
    return {'annotation_frame':'original gray source pixels, x right/y down; inferred; uncertainty ±2 final pixels',
            'regions':regions,'circles':circles,
            'landmarks':[{'id':n,'source':list(p),'canonical':list(point(p)),'type':t,'uncertain':True,'uncertainty_final_px':2} for n,p,t in landmarks],
            'openings':[{**o,'canonical':list(point(o['source']))} for o in openings],
            'component_counts':{'small_forward_engine_pods':2,'large_aft_engine_pods':2,'prominent_rear_ring':1},
            'assembly_policy':'complete assembled ship; visible turrets retained; no functional weapons added in export'}

def write_definition():
    if (ASSETS/'geometry.json').exists():
        return load_json(ASSETS/'geometry.json')
    save_json(ASSETS/'geometry.json',definition())
    return definition()

def region_mask(region,scale=1):
    m=Image.new('L',(365*scale,672*scale))
    ImageDraw.Draw(m).polygon([point(p,scale) for p in region['polygon_source']],fill=255)
    return m

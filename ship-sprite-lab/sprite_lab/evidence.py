from .core import *

def finalize():
    cfg=load_json(ROOT/'experiment.json'); times=load_json(OUT/'render-times.json')
    geometry=load_json(ASSETS/'geometry.json')
    rows=[]
    statuses={'M0':('COMPLETE','A01,A02,A03,A04','one focused tone revision'),
              'M1':('PARTIAL','A05','one focused plane shading/contact/turret revision; incomplete machinery retained'),
              'M2':('BLOCKED','','no supplied genuine mesh; no Blender'),
              'M3':('BLOCKED','','no Blender executable/bpy; entry point unexecuted'),
              'M4':('COMPLETE','A06','one actual provider attempt; structural acceptance FAIL'),
              'M5':('COMPLETE','A07','base M0 tone revision propagated; no clear small-scale gain')}
    for arm,(status,ids,note) in statuses.items():
        rows.append({'arm':arm,'status':status,'candidates':ids,'initial_active_implementation_budget_minutes':cfg['initial_effort_budget_minutes'][arm],
            'reusable_setup_time':'NOT MEASURED','ship_specific_annotation_time':'NOT MEASURED',
            'agent_active_implementation_time':'NOT MEASURED; bounded passes, no continuous per-arm timer',
            'human_original_art_preparation_time':'UNKNOWN','actual_human_cleanup_time':'NOT MEASURED',
            'actual_human_integration_correction_time':'NOT MEASURED; game test NOT RUN',
            'provider_cost':'UNKNOWN' if arm=='M4' else 'no provider call for this arm',
            'measured_processing_seconds_latest_run':sum(e['elapsed_seconds'] for e in times['events'] if e['method']==arm),
            'measured_provider_seconds':34.175 if arm=='M4' else None,'iterations_note':note})
    data={'arms':rows,'shared_setup':'scoped environment, source inventory, alpha-aware resampling, common annotation frame, technical checks and comparison generator',
          'ship_specific_preparation':{'regions':len(geometry['regions']),'landmarks':len(geometry['landmarks']),'opening_samples':len(geometry['openings']),
             'source':'agent inferred from supplied gray render; no developer correction received during run'},
          'latency_is_not_labor':True,'accepted_ships_per_human_hour':'NOT ESTABLISHED: cleanup time unmeasured and game acceptance incomplete',
          'game_load':'NOT RUN','fleet_generalization':'UNTESTED; no distinct second Star Citizen ship supplied',
          'missing':['genuine Idris mesh/maps','Blender executable/bpy','editable friend source','second distinct ship input',
                     'interactive game capture/control','developer visual ratings','measured human preparation/cleanup/integration effort'],
          'source_docs_access':'Fractal Softworks and Blender manual opens failed; see docs/RESULTS.md for successful primary reading and access limits'}
    save_json(OUT/'effort.json',data)
    if (ASSETS/'review.json').exists():
        review=load_json(ASSETS/'review.json')
        current={p.stem:sha(p) for p in sorted(OUT.glob('A[0-9][0-9].png'))}
        if 'reviewed_output_hashes' not in review: review['reviewed_output_hashes']=current
        review['review_stale']=review['reviewed_output_hashes']!=current
        save_json(ASSETS/'review.json',review)
    (OUT/'review.md').write_text('# Idris experiment\n\nSee [the full evidence, ratings and recommendation](../../docs/RESULTS.md), '
        '[technical gates](validation.json), [effort](effort.json) and [visual report](report.html).\n\n'
        'Recommendation: A04 / M0 for geometry-preserving image-only finishing. Game load NOT RUN; fleet generalization UNTESTED.\n',encoding='utf-8')

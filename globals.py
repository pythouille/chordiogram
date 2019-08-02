degrees = ['I','IIb','II','IIIb','III','IV','Vb','V','VIb','VI','VIIb','VII']

discr_deg = ['III','IIIb','VII','VIIb','V','Vb'] #discriminatory degrees

notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

name_jazz5 = ['maj','min','dom','dim','hdim7','N']

root_subst = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2,
    'D#': 3, 'Eb': 3, 'E': 4, 'Fb': 4,
    'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
    'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11,
    'B#': 0, 'N': 0}


track_list = [
    '../sounds/airegin.flac',
    '../sounds/all_alone.flac',
    '../sounds/bags_groove.flac',
    '../sounds/big_butter_and_eggman.flac',
    '../sounds/bikini.flac',
    '../sounds/black_and_tan_fantasy.flac',
    '../sounds/black_bottom_stomp.flac',
    '../sounds/black_water_blues.flac',
    '../sounds/blue_7.flac',
    '../sounds/blue_horizon.flac',
    '../sounds/blue_serge.flac',
    '../sounds/blues_for_alice.mp3',
    '../sounds/blues_in_the_closet.flac',
    '../sounds/body_and_soul(goodman).flac',
    '../sounds/body_and_soul(hawkins).flac',
    '../sounds/boplicity.flac',
    '../sounds/breakfast_feud.flac',
    '../sounds/concerto_for_cootie.flac',
    '../sounds/cotton_tail.flac',
    '../sounds/cotton_tail_fitzgerald.flac',
    '../sounds/crazeology.flac',
    '../sounds/daahoud.flac',
    '../sounds/dead_man_blues.flac',
    '../sounds/dexter_rides_again.flac',
    '../sounds/diminuendo_and_crescendo_in_blue.flac',
    '../sounds/dinah.flac',
    '../sounds/dinah_fats_waller.flac',
    '../sounds/dinah_red_nichols.flac',
    '../sounds/dippermouth_blues.flac',
    '../sounds/django.flac',
    '../sounds/doggin_around.flac',
    '../sounds/east_st_louis.flac',
    '../sounds/embraceable_you.flac',
    '../sounds/everybody_loves_my_baby.flac',
    '../sounds/evidence.flac',
    '../sounds/for_dancers_only.flac',
    '../sounds/four_brothers.flac',
    '../sounds/four_or_five_times.flac',
    '../sounds/from_monday_on.flac',
    '../sounds/giant_steps.flac',
    '../sounds/girl_from_ipanema.flac',
    '../sounds/grandpas_spells.flac',
    '../sounds/haig_and_haig.flac',
    '../sounds/handful_of_riffs.flac',
    '../sounds/harlem_congo.flac',
    '../sounds/he_s_funny_that_way.flac',
    '../sounds/honeysuckle_rose.flac',
    '../sounds/honky_tonk_train.flac',
    '../sounds/hotter_than_that.flac',
    '../sounds/i_cant_believe_you_are_in_love_with_me.flac',
    '../sounds/i_cant_get_started.flac',
    '../sounds/i_found_a_new_baby.flac',
    '../sounds/i_got_rhythm.flac',
    '../sounds/i_gotta_right_to_sing_the_blues.flac',
    '../sounds/in_a_mellotone.flac',
    '../sounds/in_gloryland.flac',
    '../sounds/indiana.flac',
    '../sounds/isfahan.flac',
    '../sounds/king_porter_stomp.flac',
    '../sounds/ko-ko(ellington).flac',
    '../sounds/lady_bird.flac',
    '../sounds/lester_leaps_in.flac',
    '../sounds/livery_stable_blues.flac',
    '../sounds/lost_your_head_blues.flac',
    '../sounds/manteca.flac',
    '../sounds/maple_leaf_rag(bechet).flac',
    '../sounds/maple_leaf_rag(braxton).flac',
    '../sounds/maple_leaf_rag(hyman).flac',
    '../sounds/mean_to_me.flac',
    '../sounds/minor_swing.flac',
    '../sounds/misterioso.flac',
    '../sounds/moanin.flac',
    '../sounds/moten_swing.flac',
    '../sounds/my_favorite_things.flac',
    '../sounds/new_east_st_louis.flac',
    '../sounds/night_in_tunisia.flac',
    '../sounds/oh_lady_be_good.flac',
    '../sounds/one_by_one.flac',
    '../sounds/one_oclock_jump.flac',
    '../sounds/organ_grinders_swing.flac',
    '../sounds/parkers_mood.flac',
    '../sounds/pentup_house.flac',
    '../sounds/potato_head_blues.flac',
    '../sounds/riverboat_shuffle.flac',
    '../sounds/rockin_chair.flac',
    '../sounds/september_in_the_rain.flac',
    '../sounds/shaw_nuff.flac',
    '../sounds/singin_the_blues.flac',
    '../sounds/st_louis_blues.flac',
    '../sounds/st_thomas.flac',
    '../sounds/stompin_at_the_savoy.flac',
    '../sounds/struttin_with_some_barbecue.flac',
    '../sounds/subconscious_lee.flac',
    '../sounds/summertime.flac',
    '../sounds/sweethearts_on_parade.flac',
    '../sounds/swing_that_music.flac',
    '../sounds/thats_a_serious_thing.flac',
    '../sounds/the_golden_bullet.flac',
    '../sounds/the_man_i_love.flac',
    '../sounds/the_preacher.flac',
    '../sounds/the_stampede.flac',
    '../sounds/these_foolish_things.flac',
    '../sounds/tricroism.flac',
    '../sounds/walkin_shoes.flac',
    '../sounds/watermelon_man.flac',
    '../sounds/weather_bird.flac',
    '../sounds/west_coast_blues.flac',
    '../sounds/west_end_blues.flac',
    '../sounds/when_lights_are_low.flac',
    '../sounds/work_song.flac',
    '../sounds/wrap_your_troubles_in_dreams.flac',
    '../sounds/wrappin_it_up.flac',
    '../sounds/you_d_be_so_nice_to_come_home_to.flac'
        ]

annotation_list = [
    '../json/airegin.json',
    '../json/all_alone.json',
    '../json/bags_groove.json',
    '../json/big_butter_and_eggman.json',
    '../json/bikini.json',
    '../json/black_and_tan_fantasy.json',
    '../json/black_bottom_stomp.json',
    '../json/black_water_blues.json',
    '../json/blue_7.json',
    '../json/blue_horizon.json',
    '../json/blue_serge.json',
    '../json/blues_for_alice.json',
    '../json/blues_in_the_closet.json',
    '../json/body_and_soul(goodman).json',
    '../json/body_and_soul(hawkins).json',
    '../json/boplicity.json',
    '../json/breakfast_feud.json',
    '../json/concerto_for_cootie.json',
    '../json/cotton_tail.json',
    '../json/cotton_tail_fitzgerald.json',
    '../json/crazeology.json',
    '../json/daahoud.json',
    '../json/dead_man_blues.json',
    '../json/dexter_rides_again.json',
    '../json/diminuendo_and_crescendo_in_blue.json',
    '../json/dinah.json',
    '../json/dinah_fats_waller.json',
    '../json/dinah_red_nichols.json',
    '../json/dippermouth_blues.json',
    '../json/django.json',
    '../json/doggin_around.json',
    '../json/east_st_louis.json',
    '../json/embraceable_you.json',
    '../json/everybody_loves_my_baby.json',
    '../json/evidence.json',
    '../json/for_dancers_only.json',
    '../json/four_brothers.json',
    '../json/four_or_five_times.json',
    '../json/from_monday_on.json',
    '../json/giant_steps.json',
    '../json/girl_from_ipanema.json',
    '../json/grandpas_spells.json',
    '../json/haig_and_haig.json',
    '../json/handful_of_riffs.json',
    '../json/harlem_congo.json',
    '../json/he_s_funny_that_way.json',
    '../json/honeysuckle_rose.json',
    '../json/honky_tonk_train.json',
    '../json/hotter_than_that.json',
    '../json/i_cant_believe_you_are_in_love_with_me.json',
    '../json/i_cant_get_started.json',
    '../json/i_found_a_new_baby.json',
    '../json/i_got_rhythm.json',
    '../json/i_gotta_right_to_sing_the_blues.json',
    '../json/in_a_mellotone.json',
    '../json/in_gloryland.json',
    '../json/indiana.json',
    '../json/isfahan.json',
    '../json/king_porter_stomp.json',
    '../json/ko-ko(ellington).json',
    '../json/lady_bird.json',
    '../json/lester_leaps_in.json',
    '../json/livery_stable_blues.json',
    '../json/lost_your_head_blues.json',
    '../json/manteca.json',
    '../json/maple_leaf_rag(bechet).json',
    '../json/maple_leaf_rag(braxton).json',
    '../json/maple_leaf_rag(hyman).json',
    '../json/mean_to_me.json',
    '../json/minor_swing.json',
    '../json/misterioso.json',
    '../json/moanin.json',
    '../json/moten_swing.json',
    '../json/my_favorite_things.json',
    '../json/new_east_st_louis.json',
    '../json/night_in_tunisia.json',
    '../json/oh_lady_be_good.json',
    '../json/one_by_one.json',
    '../json/one_oclock_jump.json',
    '../json/organ_grinders_swing.json',
    '../json/parkers_mood.json',
    '../json/pentup_house.json',
    '../json/potato_head_blues.json',
    '../json/riverboat_shuffle.json',
    '../json/rockin_chair.json',
    '../json/september_in_the_rain.json',
    '../json/shaw_nuff.json',
    '../json/singin_the_blues.json',
    '../json/st_louis_blues.json',
    '../json/st_thomas.json',
    '../json/stompin_at_the_savoy.json',
    '../json/struttin_with_some_barbecue.json',
    '../json/subconscious_lee.json',
    '../json/summertime.json',
    '../json/sweethearts_on_parade.json',
    '../json/swing_that_music.json',
    '../json/thats_a_serious_thing.json',
    '../json/the_golden_bullet.json',
    '../json/the_man_i_love.json',
    '../json/the_preacher.json',
    '../json/the_stampede.json',
    '../json/these_foolish_things.json',
    '../json/tricroism.json',
    '../json/walkin_shoes.json',
    '../json/watermelon_man.json',
    '../json/weather_bird.json',
    '../json/west_coast_blues.json',
    '../json/west_end_blues.json',
    '../json/when_lights_are_low.json',
    '../json/work_song.json',
    '../json/wrap_your_troubles_in_dreams.json',
    '../json/wrappin_it_up.json',
    '../json/you_d_be_so_nice_to_come_home_to.json'
        ]



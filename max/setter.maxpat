{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 6,
			"revision" : 5,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 69.0, 87.0, 726.0, 634.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "",
		"digest" : "",
		"tags" : "",
		"style" : "",
		"subpatcher_template" : "dark_template",
		"assistshowspatchername" : 0,
		"boxes" : [ 			{
				"box" : 				{
					"id" : "obj-16",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 359.0, 12.0, 150.0, 20.0 ],
					"text" : "Adaptiverb"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-14",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 40.0, 12.0, 150.0, 20.0 ],
					"text" : "OB-Xd"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-10",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 327.0, 134.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-8",
					"items" : [ "/adaptiverb/predelay", ",", "/adaptiverb/lowCut", ",", "/adaptiverb/air", ",", "/adaptiverb/richness", ",", "/adaptiverb/reverbModel", ",", "/adaptiverb/sustain", ",", "/adaptiverb/reverbMix", ",", "/adaptiverb/reverbSource", ",", "/adaptiverb/reverbSize", ",", "/adaptiverb/wetGain", ",", "/adaptiverb/drywetMix", ",", "/adaptiverb/hcfAmt", ",", "/adaptiverb/reverbDamp", ",", "/adaptiverb/simplify", ",", "/adaptiverb/interval", ",", "/adaptiverb/pRandomize", ",", "/adaptiverb/diffusion", ",", "/adaptiverb/breathiness", ",", "/adaptiverb/hcfMode", ",", "/adaptiverb/hcfWeighting", ",", "/adaptiverb/trackingMode", ",", "/adaptiverb/kybdAlgo", ",", "/adaptiverb/snapshot", ",", "/adaptiverb/freeze" ],
					"maxclass" : "umenu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "int", "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 359.0, 36.0, 190.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-2",
					"maxclass" : "flonum",
					"maximum" : 1.0,
					"minimum" : 0.0,
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 243.0, 135.0, 50.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-20",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 40.0, 99.0, 29.5, 22.0 ],
					"text" : "+ 1"
				}

			}
, 			{
				"box" : 				{
					"fontsize" : 18.0,
					"id" : "obj-19",
					"maxclass" : "number",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 40.0, 179.0, 60.0, 29.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-15",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 125.0, 225.0, 45.0, 22.0 ],
					"text" : "list.join"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-12",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"patching_rect" : [ 125.0, 99.0, 137.0, 22.0 ],
					"text" : "t s b"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-11",
					"items" : [ "/OB-Xd/volume", ",", "/OB-Xd/tune", ",", "/OB-Xd/octave", ",", "/OB-Xd/voiceDetune", ",", "/OB-Xd/unison", ",", "/OB-Xd/portamento", ",", "/OB-Xd/osc1Pitch", ",", "/OB-Xd/pulseWidth", ",", "/OB-Xd/osc2Pitch", ",", "/OB-Xd/osc1Saw", ",", "/OB-Xd/osc1Pulse", ",", "/OB-Xd/osc2Detune", ",", "/OB-Xd/osc2Saw", ",", "/OB-Xd/osc2Pulse", ",", "/OB-Xd/osc2HS", ",", "/OB-Xd/xmod", ",", "/OB-Xd/pQuant", ",", "/OB-Xd/brightness", ",", "/OB-Xd/env2pitch", ",", "/OB-Xd/osc1Mix", ",", "/OB-Xd/osc2Mix", ",", "/OB-Xd/noiseMix", ",", "/OB-Xd/bendRange", ",", "/OB-Xd/bend2osc", ",", "/OB-Xd/vibratoRate", ",", "/OB-Xd/VFltFactor", ",", "/OB-Xd/VAmpFactor", ",", "/OB-Xd/cutoff", ",", "/OB-Xd/resonance", ",", "/OB-Xd/fEnvAmt", ",", "/OB-Xd/fKeyFollow", ",", "/OB-Xd/fWarm", ",", "/OB-Xd/multimode", ",", "/OB-Xd/bpassBlend", ",", "/OB-Xd/fourPole", ",", "/OB-Xd/lfoFreq", ",", "/OB-Xd/lfoAmt1", ",", "/OB-Xd/lfoAmt2", ",", "/OB-Xd/lfoSine", ",", "/OB-Xd/lfoOsc1", ",", "/OB-Xd/lfoPw1", ",", "/OB-Xd/lfoSquare", ",", "/OB-Xd/lfoOsc2", ",", "/OB-Xd/lfoPw2", ",", "/OB-Xd/lfoSAH", ",", "/OB-Xd/lfoFilter", ",", "/OB-Xd/fAttack", ",", "/OB-Xd/fDecay", ",", "/OB-Xd/fSustain", ",", "/OB-Xd/fRelease", ",", "/OB-Xd/attack", ",", "/OB-Xd/decay", ",", "/OB-Xd/sustain", ",", "/OB-Xd/release", ",", "/OB-Xd/fDetune", ",", "/OB-Xd/pDetune", ",", "/OB-Xd/eDetune", ",", "/OB-Xd/pan1", ",", "/OB-Xd/pan2", ",", "/OB-Xd/pan3", ",", "/OB-Xd/pan4", ",", "/OB-Xd/pan5", ",", "/OB-Xd/pan6", ",", "/OB-Xd/pan7", ",", "/OB-Xd/pan8" ],
					"maxclass" : "umenu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "int", "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 40.0, 36.0, 190.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 125.0, 331.0, 137.0, 22.0 ],
					"text" : "udpsend 127.0.0.1 9110"
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-15", 0 ],
					"midpoints" : [ 336.5, 218.0, 134.5, 218.0 ],
					"source" : [ "obj-10", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 0 ],
					"source" : [ "obj-11", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-20", 0 ],
					"source" : [ "obj-11", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-15", 0 ],
					"source" : [ "obj-12", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-12", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-15", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-15", 1 ],
					"midpoints" : [ 252.5, 212.5, 160.5, 212.5 ],
					"source" : [ "obj-2", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-19", 0 ],
					"source" : [ "obj-20", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 0 ],
					"disabled" : 1,
					"midpoints" : [ 454.0, 84.0, 134.5, 84.0 ],
					"source" : [ "obj-8", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-20", 0 ],
					"disabled" : 1,
					"midpoints" : [ 368.5, 84.0, 49.5, 84.0 ],
					"source" : [ "obj-8", 0 ]
				}

			}
 ],
		"dependency_cache" : [  ],
		"autosave" : 0,
		"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
		"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
	}

}

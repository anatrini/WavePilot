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
		"rect" : [ 34.0, 100.0, 724.0, 747.0 ],
		"bglocked" : 0,
		"openinpresentation" : 1,
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
					"id" : "obj-13",
					"linecount" : 18,
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 391.0, 167.0, 152.0, 248.0 ],
					"presentation" : 1,
					"presentation_linecount" : 12,
					"presentation_rect" : [ 353.0, 48.0, 268.0, 167.0 ],
					"text" : "1. Ottieni preset\n2. Fai ottimizzazione\n3. Usa il log dell'ottimizzazione per il t\n\n\n1. Get presets\n2. Run optimisation\n3. Pass optimization log file during the train\n4. Open the host (Reaper, Max, Td...)\n5. Set port 8888 and IP on smartdevice\n6. Open the controller and set interaction mode\n7. Normalised values are sent back to port 9108"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 3,
					"fontname" : "Graphik",
					"fontsize" : 30.0,
					"id" : "obj-88",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 79.0, 1024.0, 404.0, 46.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 4.0, 3.0, 335.772722721099854, 46.0 ],
					"saved_attribute_attributes" : 					{
						"textcolor" : 						{
							"expression" : "themecolor.live_alert"
						}

					}
,
					"text" : "WavePilot Controller",
					"textcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"textjustification" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-83",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 457.600006818771362, 604.0, 33.0, 22.0 ],
					"text" : "== 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-82",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 54.400000810623169, 771.200011491775513, 82.599999964237213, 22.0 ],
					"text" : "gate 1 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-80",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "FullPacket" ],
					"patching_rect" : [ 232.0, 755.200011253356934, 84.0, 22.0 ],
					"text" : "o.pack /cursor"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-78",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "FullPacket" ],
					"patching_rect" : [ 232.0, 728.000010848045349, 120.0, 22.0 ],
					"text" : "o.route /source/1/xyz"
				}

			}
, 			{
				"box" : 				{
					"activebgoncolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"fontname" : "Graphik",
					"fontsize" : 12.0,
					"id" : "obj-77",
					"maxclass" : "live.text",
					"mode" : 0,
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 357.0, 793.799999833106995, 80.800001204013824, 22.400000333786011 ],
					"presentation" : 1,
					"presentation_rect" : [ 268.0, 52.0, 70.909088373184204, 50.909089088439941 ],
					"saved_attribute_attributes" : 					{
						"activebgoncolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"valueof" : 						{
							"parameter_enum" : [ "val1", "val2" ],
							"parameter_longname" : "live.text",
							"parameter_mmax" : 1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "live.text",
							"parameter_type" : 2
						}

					}
,
					"text" : "open view",
					"varname" : "live.text"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-84",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 156.000002324581146, 840.0, 121.0, 22.0 ],
					"text" : "/window/openorclose"
				}

			}
, 			{
				"box" : 				{
					"activebgcolor" : [ 0.2, 0.2, 0.2, 1.0 ],
					"activebgoncolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"bgcolor" : [ 0.0, 0.0, 0.0, 0.5 ],
					"bordercolor" : [ 0.0, 0.0, 0.0, 0.0 ],
					"focusbordercolor" : [ 0.0, 0.0, 0.0, 0.5 ],
					"id" : "obj-70",
					"maxclass" : "live.toggle",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 54.400000810623169, 681.0, 28.399994671344757, 27.200000405311584 ],
					"presentation" : 1,
					"presentation_rect" : [ 214.0, 496.0, 28.399994671344757, 27.200000405311584 ],
					"rounded" : 18.0,
					"saved_attribute_attributes" : 					{
						"activebgcolor" : 						{
							"expression" : ""
						}
,
						"activebgoncolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"bgcolor" : 						{
							"expression" : ""
						}
,
						"bordercolor" : 						{
							"expression" : ""
						}
,
						"focusbordercolor" : 						{
							"expression" : ""
						}
,
						"valueof" : 						{
							"parameter_enum" : [ "off", "on" ],
							"parameter_longname" : "live.toggle",
							"parameter_mmax" : 1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "live.toggle",
							"parameter_type" : 2
						}

					}
,
					"varname" : "live.toggle"
				}

			}
, 			{
				"box" : 				{
					"activedialcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"focusbordercolor" : [ 0.0, 0.019608, 0.078431, 0.0 ],
					"fontname" : "Graphik",
					"id" : "obj-67",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 915.0, 14.0, 42.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 283.0, 399.0, 42.0, 51.0 ],
					"saved_attribute_attributes" : 					{
						"activedialcolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"focusbordercolor" : 						{
							"expression" : ""
						}
,
						"valueof" : 						{
							"parameter_initial" : [ 1 ],
							"parameter_initial_enable" : 1,
							"parameter_linknames" : 1,
							"parameter_longname" : "scale",
							"parameter_mmax" : 100.0,
							"parameter_mmin" : 0.1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "scale",
							"parameter_type" : 0,
							"parameter_unitstyle" : 1
						}

					}
,
					"varname" : "scale"
				}

			}
, 			{
				"box" : 				{
					"activedialcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"fontname" : "Graphik",
					"id" : "obj-62",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 523.5, 21.0, 43.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 160.0, 485.0, 43.0, 51.0 ],
					"saved_attribute_attributes" : 					{
						"activedialcolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"valueof" : 						{
							"parameter_longname" : "metro",
							"parameter_mmax" : 5000.0,
							"parameter_modmode" : 3,
							"parameter_shortname" : "metro",
							"parameter_type" : 0,
							"parameter_unitstyle" : 0
						}

					}
,
					"varname" : "metro"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-45",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 1379.0, 48.5, 58.0, 22.0 ],
					"text" : "loadbang"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-44",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 6,
							"revision" : 5,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 61.0, 100.0, 640.0, 480.0 ],
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
						"boxes" : [ 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-2",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 122.0, 367.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-1",
									"index" : 1,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "bang" ],
									"patching_rect" : [ 50.0, 49.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-43",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "bang", "bang" ],
									"patching_rect" : [ 50.0, 134.0, 91.0, 22.0 ],
									"text" : "b 2"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-41",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 50.0, 100.0, 54.0, 22.0 ],
									"text" : "deferlow"
								}

							}
, 							{
								"box" : 								{
									"fontface" : 0,
									"id" : "obj-40",
									"linecount" : 10,
									"maxclass" : "o.compose",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 122.0, 169.0, 182.0, 139.0 ],
									"saved_bundle_data" : [ 35, 98, 117, 110, 100, 108, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 47, 116, 121, 112, 101, 0, 0, 0, 44, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 47, 97, 99, 99, 101, 108, 0, 0, 44, 105, 105, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 47, 103, 121, 114, 111, 0, 0, 0, 44, 105, 105, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 47, 99, 111, 109, 112, 97, 115, 115, 0, 0, 0, 0, 44, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 47, 104, 105, 115, 116, 111, 114, 121, 65, 110, 103, 108, 101, 88, 0, 0, 44, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 47, 104, 105, 115, 116, 111, 114, 121, 65, 110, 103, 108, 101, 89, 0, 0, 44, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 47, 104, 105, 115, 116, 111, 114, 121, 65, 110, 103, 108, 101, 90, 0, 0, 44, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 47, 115, 99, 97, 108, 105, 110, 103, 70, 97, 99, 116, 111, 114, 0, 0, 44, 100, 0, 0, 63, -16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 47, 116, 111, 117, 99, 104, 48, 0, 44, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 47, 116, 111, 117, 99, 104, 102, 111, 114, 99, 101, 48, 0, 0, 0, 0, 44, 100, 0, 0, 63, -12, 0, 0, 0, 0, 0, 0 ],
									"saved_bundle_length" : 304,
									"text" : "/type : 0,\n/accel : [0, 0, 0],\n/gyro : [0, 0, 0],\n/compass : 0,\n/historyAngleX : 0,\n/historyAngleY : 0,\n/historyAngleZ : 0,\n/scalingFactor : 1.,\n/touch0 : [0., 0.],\n/touchforce0 : 1.25"
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-41", 0 ],
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-2", 0 ],
									"source" : [ "obj-40", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-43", 0 ],
									"source" : [ "obj-41", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-40", 0 ],
									"source" : [ "obj-43", 1 ]
								}

							}
 ],
						"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
					}
,
					"patching_rect" : [ 1379.0, 81.5, 116.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ],
						"globalpatchername" : "",
						"locked_bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"tags" : ""
					}
,
					"text" : "p init"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 0,
					"id" : "obj-38",
					"linecount" : 52,
					"maxclass" : "o.expr.codebox",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "FullPacket", "FullPacket" ],
					"patching_rect" : [ 799.0, 164.0, 555.0, 684.0 ],
					"text" : "/historyAngleX = 0,\n/historyAngleY = 0,\n/historyAngleZ = 0,\n\n### IMU with fusion filter (accelerometer, gyroscope, compass)\nif( /type == 0,\n  progn(\n    /delta = 0.0333, # update rate (30Hz)\n    /alpha = 0.98, # constant value for complementary filter\n\n    /normAccel = /accel / 9.81, \n    /normCompass = (/compass[[ 0 ]] - 180) / 180,\n\t\t\t\n    ### Estimate accelerometer angles\n    /accelAngleX = atan2(/normAccel[[ 1 ]], /normAccel[[ 2 ]]),\n    /accelAngleY = atan2(/normAccel[[ 0 ]], /normAccel[[ 2 ]]),\n    /accelAngleZ = 0, #accel cannot measure rotation on z axis\n\n    ### Integrate angular velocity of gyroscope in time\n    /gyroAngleX = /historyAngleX + (/gyro[[ 0 ]] * /delta),\n    /gyroAngleY = /historyAngleY + (/gyro[[ 1 ]] * /delta),\n    /gyroAngleZ = /historyAngleZ + (/gyro[[ 2 ]] * /delta),\n\n    ### Apply complementary filter\n    /filterAngleX = /alpha * /gyroAngleX + (1 - /alpha) * /accelAngleX,\n    /filterAngleY = /alpha * /gyroAngleY + (1 - /alpha) * /accelAngleY,\n    /filterAngleZ = /alpha * /gyroAngleZ + (1 - /alpha) * /normCompass,\n\n    /posX = /filterAngleX / pi() * /scalingFactor,\n    /posY = /filterAngleY / pi() * /scalingFactor,\n    /posZ = -1 * /filterAngleZ / pi() * /scalingFactor,\n    \n    /cursor = [/posZ, /posY, /posX],\n\n    /historyAngleX = /filterAngleX,\n    /historyAngleY = /filterAngleY,\n    /historyAngleZ = /filterAngleZ\n  ),\n  progn(\n    /min = -1.0,\n    /max = 1.0,\n    /touchforce0_max = 2.5,\n\n    /posX = /touch0[[ 0 ]],\n    /posY = /touch0[[ 1 ]] * -1,\n    /posZ = scale(/touchforce0, 0.0, /touchforce0_max, /max, /min),\n \n    /cursor = [/posX, /posY, /posZ] * /scalingFactor\n  )\n),\n### To display in spat viewer\n/source/1/xyz = /cursor"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-36",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "FullPacket" ],
					"patching_rect" : [ 1243.0, 81.5, 73.0, 22.0 ],
					"text" : "o.pack /type"
				}

			}
, 			{
				"box" : 				{
					"activebgoncolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"fontname" : "Graphik",
					"fontsize" : 12.0,
					"id" : "obj-33",
					"maxclass" : "live.tab",
					"num_lines_patching" : 2,
					"num_lines_presentation" : 2,
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 1243.0, 12.5, 83.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 275.0, 308.0, 58.181816101074219, 71.818179249763489 ],
					"saved_attribute_attributes" : 					{
						"activebgoncolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"valueof" : 						{
							"parameter_enum" : [ "Gyro", "Pressure" ],
							"parameter_longname" : "live.tab[2]",
							"parameter_mmax" : 1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "live.tab[1]",
							"parameter_type" : 2,
							"parameter_unitstyle" : 9
						}

					}
,
					"varname" : "live.tab[2]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-2",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 799.0, 127.0, 54.0, 22.0 ],
					"text" : "o.accum"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-15",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "FullPacket" ],
					"patching_rect" : [ 915.0, 81.5, 122.0, 22.0 ],
					"text" : "o.pack /scalingFactor"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-6",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "FullPacket" ],
					"patching_rect" : [ 1228.0, 947.0, 86.0, 22.0 ],
					"text" : "o.route /cursor"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-5",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "FullPacket" ],
					"patching_rect" : [ 682.0, 81.5, 107.0, 22.0 ],
					"text" : "o.route /deviceinfo"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-100",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 523.0, 730.0, 29.5, 22.0 ],
					"text" : "+ 1"
				}

			}
, 			{
				"box" : 				{
					"activebgoncolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"fontname" : "Graphik",
					"fontsize" : 12.0,
					"id" : "obj-99",
					"maxclass" : "live.tab",
					"num_lines_patching" : 2,
					"num_lines_presentation" : 2,
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 523.0, 480.0, 107.20000159740448, 51.200000762939453 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 52.0, 260.9090815782547, 50.909089088439941 ],
					"saved_attribute_attributes" : 					{
						"activebgoncolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"valueof" : 						{
							"parameter_enum" : [ "SPAT", "SMARTD" ],
							"parameter_longname" : "live.tab[1]",
							"parameter_mmax" : 1,
							"parameter_modmode" : 0,
							"parameter_shortname" : "live.tab[1]",
							"parameter_type" : 2,
							"parameter_unitstyle" : 9
						}

					}
,
					"varname" : "live.tab[1]"
				}

			}
, 			{
				"box" : 				{
					"flash_color" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"fontface" : 0,
					"id" : "obj-96",
					"maxclass" : "o.display",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 697.0, 936.0, 436.0, 33.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 4.0, 716.0, 335.454533457756042, 33.0 ],
					"saved_attribute_attributes" : 					{
						"flash_color" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"textcolor" : 						{
							"expression" : "themecolor.live_alert"
						}

					}
,
					"text" : "/cursor : [0.440395, -0.496435, -0.748068]",
					"textcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-95",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 523.0, 794.0, 42.0, 22.0 ],
					"text" : "switch"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-86",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "FullPacket" ],
					"patching_rect" : [ 118.0, 448.0, 115.0, 22.0 ],
					"text" : "o.prepend /source/1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-81",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 118.0, 412.0, 100.0, 22.0 ],
					"text" : "spat5.trajectories"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-79",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "FullPacket" ],
					"patching_rect" : [ 579.0, 755.200011253356934, 164.0, 22.0 ],
					"text" : "o.select /cursor /source/1/xyz"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-60",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "FullPacket" ],
					"patching_rect" : [ 682.0, 46.5, 213.0, 22.0 ],
					"text" : "o.route /ZIGSIM/00KWhGqPVfKH51Xf"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-35",
					"linecount" : 3,
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"patching_rect" : [ 118.0, 881.600013136863708, 281.0, 49.0 ],
					"saved_object_attributes" : 					{
						"parameter_enable" : 0
					}
,
					"text" : "spat5.viewer @initwith \"/source/number 1, /layout single, /window/size 600 600, /source/1/color blue, /listener/visible 0, /display/zoom 50\""
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-29",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 533.0, 77.0, 119.0, 22.0 ],
					"text" : "metro 500 @active 1"
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-30",
					"lockeddragscroll" : 0,
					"lockedsize" : 0,
					"maxclass" : "bpatcher",
					"name" : "spat5.scaling.maxpat",
					"numinlets" : 1,
					"numoutlets" : 1,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "" ],
					"patching_rect" : [ 118.0, 480.0, 150.0, 75.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 295.0, 150.400002241134644, 80.800001204013824 ],
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-25",
					"lockeddragscroll" : 0,
					"lockedsize" : 0,
					"maxclass" : "bpatcher",
					"name" : "spat5.rotation.maxpat",
					"numinlets" : 1,
					"numoutlets" : 1,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "" ],
					"patching_rect" : [ 118.0, 635.0, 150.400002241134644, 83.200001239776611 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 378.0, 150.400002241134644, 80.800001204013824 ],
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-28",
					"lockeddragscroll" : 0,
					"lockedsize" : 0,
					"maxclass" : "bpatcher",
					"name" : "spat5.translation.maxpat",
					"numinlets" : 1,
					"numoutlets" : 1,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "" ],
					"patching_rect" : [ 118.0, 556.0, 150.400002241134644, 76.80000114440918 ],
					"presentation" : 1,
					"presentation_rect" : [ 4.0, 463.0, 151.600002259016037, 80.800001204013824 ],
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-18",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 118.0, 235.0, 29.0, 22.0 ],
					"text" : "thru"
				}

			}
, 			{
				"box" : 				{
					"activebgoncolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"fontname" : "Graphik",
					"id" : "obj-14",
					"maxclass" : "live.tab",
					"num_lines_patching" : 10,
					"num_lines_presentation" : 10,
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 10.0, 16.5, 235.0, 132.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 104.0, 335.0, 188.0 ],
					"saved_attribute_attributes" : 					{
						"activebgoncolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"valueof" : 						{
							"parameter_enum" : [ "viviani", "steinmetz", "clelia", "sphericalhelix", "satellite", "sphericalsinusoid", "rhumbline", "moebius", "seamlinetennisball", "hypotrochoid", "epitrochoid", "cylindricsinewave", "squareknot", "grannyknot", "conicalrose", "basin", "archytascurve", "sphericalcycloid", "sphericalellipse" ],
							"parameter_longname" : "live.tab",
							"parameter_mmax" : 18,
							"parameter_modmode" : 0,
							"parameter_shortname" : "live.tab",
							"parameter_type" : 2,
							"parameter_unitstyle" : 9
						}

					}
,
					"varname" : "live.tab"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 467.0, 77.0, 35.0, 22.0 ],
					"text" : "/b $1"
				}

			}
, 			{
				"box" : 				{
					"activedialcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"focusbordercolor" : [ 0.0, 0.019608, 0.078431, 0.0 ],
					"fontname" : "Graphik",
					"id" : "obj-16",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 467.0, 21.0, 42.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 207.0, 399.0, 42.0, 51.0 ],
					"saved_attribute_attributes" : 					{
						"activedialcolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"focusbordercolor" : 						{
							"expression" : ""
						}
,
						"valueof" : 						{
							"parameter_initial" : [ 1 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "live.dial[19]",
							"parameter_mmax" : 15.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "b",
							"parameter_type" : 0,
							"parameter_unitstyle" : 1
						}

					}
,
					"varname" : "live.dial[2]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-9",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 399.0, 77.0, 35.0, 22.0 ],
					"text" : "/a $1"
				}

			}
, 			{
				"box" : 				{
					"activedialcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"focusbordercolor" : [ 0.0, 0.019608, 0.078431, 0.0 ],
					"fontname" : "Graphik",
					"id" : "obj-10",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 399.0, 21.0, 42.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 160.0, 399.0, 42.0, 51.0 ],
					"saved_attribute_attributes" : 					{
						"activedialcolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"focusbordercolor" : 						{
							"expression" : ""
						}
,
						"valueof" : 						{
							"parameter_initial" : [ 1 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "live.dial[18]",
							"parameter_mmax" : 15.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "a",
							"parameter_type" : 0,
							"parameter_unitstyle" : 1
						}

					}
,
					"varname" : "live.dial[1]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-20",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 325.0, 77.0, 61.0, 22.0 ],
					"text" : "/radius $1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-19",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 255.0, 77.0, 61.0, 22.0 ],
					"text" : "/speed $1"
				}

			}
, 			{
				"box" : 				{
					"activedialcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"focusbordercolor" : [ 0.0, 0.019608, 0.078431, 0.0 ],
					"fontname" : "Graphik",
					"id" : "obj-24",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 255.0, 21.0, 46.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 158.0, 315.0, 46.0, 51.0 ],
					"saved_attribute_attributes" : 					{
						"activedialcolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"focusbordercolor" : 						{
							"expression" : ""
						}
,
						"valueof" : 						{
							"parameter_initial" : [ 50 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "live.dial[16]",
							"parameter_mmax" : 720.0,
							"parameter_mmin" : -720.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "speed",
							"parameter_type" : 0,
							"parameter_unitstyle" : 1
						}

					}
,
					"varname" : "live.dial[16]"
				}

			}
, 			{
				"box" : 				{
					"activedialcolor" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"focusbordercolor" : [ 0.0, 0.019608, 0.078431, 0.0 ],
					"fontname" : "Graphik",
					"id" : "obj-115",
					"maxclass" : "live.dial",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "float" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 325.0, 21.0, 42.0, 51.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 207.0, 315.0, 42.0, 51.0 ],
					"saved_attribute_attributes" : 					{
						"activedialcolor" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"focusbordercolor" : 						{
							"expression" : ""
						}
,
						"valueof" : 						{
							"parameter_initial" : [ 1 ],
							"parameter_initial_enable" : 1,
							"parameter_longname" : "live.dial[10]",
							"parameter_mmax" : 15.0,
							"parameter_modmode" : 0,
							"parameter_shortname" : "radius",
							"parameter_type" : 0,
							"parameter_unitstyle" : 1
						}

					}
,
					"varname" : "live.dial[10]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-68",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 118.0, 184.5, 51.0, 22.0 ],
					"text" : "/type $1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-12",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 682.0, 11.5, 142.0, 22.0 ],
					"text" : "udpreceive 8888 CNMAT"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-1",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 523.0, 852.0, 135.0, 22.0 ],
					"text" : "udpsend localhost 9108"
				}

			}
, 			{
				"box" : 				{
					"angle" : 0.0,
					"bgcolor" : [ 0.901961, 0.901961, 0.901961, 0.0 ],
					"border" : 2,
					"bordercolor" : [ 0.0, 0.0, 0.0, 0.5 ],
					"id" : "obj-85",
					"maxclass" : "panel",
					"mode" : 0,
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 67.0, 1045.0, 196.121216000000004, 65.888824 ],
					"presentation" : 1,
					"presentation_rect" : [ 268.0, 295.0, 71.218179240822792, 249.090900182723999 ],
					"proportion" : 0.39,
					"rounded" : 18
				}

			}
, 			{
				"box" : 				{
					"angle" : 0.0,
					"bgcolor" : [ 0.901961, 0.901961, 0.901961, 0.0 ],
					"border" : 2,
					"bordercolor" : [ 0.0, 0.0, 0.0, 0.5 ],
					"id" : "obj-7",
					"maxclass" : "panel",
					"mode" : 0,
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 52.0, 1030.0, 196.121216000000004, 65.888824 ],
					"presentation" : 1,
					"presentation_rect" : [ 158.0, 295.0, 107.272723436355591, 248.981813371181488 ],
					"proportion" : 0.39,
					"rounded" : 18
				}

			}
, 			{
				"box" : 				{
					"angle" : 0.0,
					"bgcolor" : [ 0.901961, 0.901961, 0.901961, 0.0 ],
					"border" : 2,
					"bordercolor" : [ 0.0, 0.0, 0.0, 0.5 ],
					"id" : "obj-4",
					"maxclass" : "panel",
					"mode" : 0,
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 77.439391999999998, 1029.999999999999773, 196.121216000000004, 65.888824 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 546.0, 334.0, 164.0 ],
					"proportion" : 0.39,
					"rounded" : 18
				}

			}
, 			{
				"box" : 				{
					"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
					"candicane2" : [ 0.093121, 0.536852, 0.511438, 1.0 ],
					"candicane3" : [ 1.0, 0.490196, 0.262745, 1.0 ],
					"candycane" : 5,
					"id" : "obj-74",
					"maxclass" : "multislider",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 1228.0, 978.0, 252.0, 135.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.0, 548.0, 334.0, 160.0 ],
					"saved_attribute_attributes" : 					{
						"candicane3" : 						{
							"expression" : "themecolor.live_alert"
						}
,
						"slidercolor" : 						{
							"expression" : "themecolor.live_value_arc"
						}

					}
,
					"setminmax" : [ -1.5, 1.5 ],
					"setstyle" : 1,
					"signed" : 1,
					"size" : 3,
					"slidercolor" : [ 0.427450980392157, 0.843137254901961, 1.0, 1.0 ]
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-9", 0 ],
					"source" : [ "obj-10", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-95", 0 ],
					"source" : [ "obj-100", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-20", 0 ],
					"source" : [ "obj-115", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-60", 0 ],
					"source" : [ "obj-12", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-68", 0 ],
					"source" : [ "obj-14", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"midpoints" : [ 924.5, 115.0, 808.5, 115.0 ],
					"source" : [ "obj-15", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-16", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-81", 0 ],
					"source" : [ "obj-18", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"midpoints" : [ 264.5, 222.0, 127.5, 222.0 ],
					"source" : [ "obj-19", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-38", 0 ],
					"source" : [ "obj-2", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"midpoints" : [ 334.5, 222.0, 127.5, 222.0 ],
					"source" : [ "obj-20", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-19", 0 ],
					"source" : [ "obj-24", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-78", 0 ],
					"midpoints" : [ 127.5, 714.000005394220352, 241.5, 714.000005394220352 ],
					"order" : 0,
					"source" : [ "obj-25", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-82", 1 ],
					"order" : 1,
					"source" : [ "obj-25", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-25", 0 ],
					"source" : [ "obj-28", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"midpoints" : [ 542.5, 222.0, 127.5, 222.0 ],
					"source" : [ "obj-29", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"midpoints" : [ 476.5, 222.0, 127.5, 222.0 ],
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-28", 0 ],
					"source" : [ "obj-30", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-36", 0 ],
					"source" : [ "obj-33", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"midpoints" : [ 1252.5, 115.0, 808.5, 115.0 ],
					"source" : [ "obj-36", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-6", 0 ],
					"order" : 0,
					"source" : [ "obj-38", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-79", 0 ],
					"midpoints" : [ 808.5, 863.0, 774.0, 863.0, 774.0, 747.0, 588.5, 747.0 ],
					"order" : 1,
					"source" : [ "obj-38", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"midpoints" : [ 1388.5, 116.0, 808.5, 116.0 ],
					"source" : [ "obj-44", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-44", 0 ],
					"source" : [ "obj-45", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-5", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-74", 0 ],
					"source" : [ "obj-6", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"source" : [ "obj-60", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 1 ],
					"midpoints" : [ 533.0, 72.5, 642.5, 72.5 ],
					"source" : [ "obj-62", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-15", 0 ],
					"source" : [ "obj-67", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"source" : [ "obj-68", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-82", 0 ],
					"source" : [ "obj-70", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-84", 0 ],
					"source" : [ "obj-77", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-80", 0 ],
					"source" : [ "obj-78", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-35", 0 ],
					"midpoints" : [ 661.0, 824.000000655651093, 127.5, 824.000000655651093 ],
					"source" : [ "obj-79", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-95", 2 ],
					"midpoints" : [ 588.5, 780.0, 555.5, 780.0 ],
					"source" : [ "obj-79", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-95", 1 ],
					"midpoints" : [ 241.5, 785.500005632638931, 544.0, 785.500005632638931 ],
					"source" : [ "obj-80", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-86", 0 ],
					"source" : [ "obj-81", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-35", 0 ],
					"source" : [ "obj-82", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-70", 0 ],
					"midpoints" : [ 467.100006818771362, 627.0, 63.900000810623169, 627.0 ],
					"source" : [ "obj-83", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-35", 0 ],
					"source" : [ "obj-84", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-30", 0 ],
					"source" : [ "obj-86", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"midpoints" : [ 408.5, 222.0, 127.5, 222.0 ],
					"source" : [ "obj-9", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-1", 0 ],
					"order" : 1,
					"source" : [ "obj-95", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-96", 0 ],
					"midpoints" : [ 532.5, 827.5, 706.5, 827.5 ],
					"order" : 0,
					"source" : [ "obj-95", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-100", 0 ],
					"order" : 0,
					"source" : [ "obj-99", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-83", 0 ],
					"order" : 1,
					"source" : [ "obj-99", 0 ]
				}

			}
 ],
		"parameters" : 		{
			"obj-10" : [ "live.dial[18]", "a", 0 ],
			"obj-115" : [ "live.dial[10]", "radius", 0 ],
			"obj-14" : [ "live.tab", "live.tab", 0 ],
			"obj-16" : [ "live.dial[19]", "b", 0 ],
			"obj-24" : [ "live.dial[16]", "speed", 0 ],
			"obj-25::obj-2" : [ "live.text[2]", "live.text", 0 ],
			"obj-25::obj-91" : [ "live.dial[12]", "angle z", 0 ],
			"obj-25::obj-92" : [ "live.dial[11]", "angle y", 0 ],
			"obj-25::obj-93" : [ "live.dial[9]", "angle x", 0 ],
			"obj-28::obj-2" : [ "live.text[1]", "live.text", 0 ],
			"obj-28::obj-91" : [ "live.dial[6]", "offset x", 0 ],
			"obj-28::obj-92" : [ "live.dial[7]", "offset y", 0 ],
			"obj-28::obj-93" : [ "live.dial[8]", "offset z", 0 ],
			"obj-30::obj-2" : [ "live.text[3]", "live.text", 0 ],
			"obj-30::obj-91" : [ "live.dial[14]", "scale x", 0 ],
			"obj-30::obj-92" : [ "live.dial[13]", "scale y", 0 ],
			"obj-30::obj-93" : [ "live.dial[17]", "scale z", 0 ],
			"obj-33" : [ "live.tab[2]", "live.tab[1]", 0 ],
			"obj-62" : [ "metro", "metro", 0 ],
			"obj-67" : [ "scale", "scale", 0 ],
			"obj-70" : [ "live.toggle", "live.toggle", 0 ],
			"obj-77" : [ "live.text", "live.text", 0 ],
			"obj-99" : [ "live.tab[1]", "live.tab[1]", 0 ],
			"parameterbanks" : 			{
				"0" : 				{
					"index" : 0,
					"name" : "",
					"parameters" : [ "-", "-", "-", "-", "-", "-", "-", "-" ]
				}

			}
,
			"parameter_overrides" : 			{
				"obj-25::obj-2" : 				{
					"parameter_longname" : "live.text[2]"
				}
,
				"obj-25::obj-91" : 				{
					"parameter_longname" : "live.dial[12]"
				}
,
				"obj-25::obj-92" : 				{
					"parameter_longname" : "live.dial[11]"
				}
,
				"obj-25::obj-93" : 				{
					"parameter_longname" : "live.dial[9]"
				}
,
				"obj-30::obj-2" : 				{
					"parameter_longname" : "live.text[3]"
				}
,
				"obj-30::obj-91" : 				{
					"parameter_longname" : "live.dial[14]"
				}
,
				"obj-30::obj-92" : 				{
					"parameter_longname" : "live.dial[13]"
				}
,
				"obj-30::obj-93" : 				{
					"parameter_longname" : "live.dial[17]"
				}

			}
,
			"inherited_shortname" : 1
		}
,
		"dependency_cache" : [ 			{
				"name" : "o.accum.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/odot/patchers/namespace",
				"patcherrelativepath" : "../../../Max 8/Packages/odot/patchers/namespace",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "o.compose.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.display.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.expr.codebox.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.pack.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.prepend.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.route.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.select.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "o.union.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "spat5.osc.routepass.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "spat5.rotation.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/spat5/patchers",
				"patcherrelativepath" : "../../../Max 8/Packages/spat5/patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "spat5.scaling.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/spat5/patchers",
				"patcherrelativepath" : "../../../Max 8/Packages/spat5/patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "spat5.trajectories.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "spat5.transform.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "spat5.translation.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/spat5/patchers",
				"patcherrelativepath" : "../../../Max 8/Packages/spat5/patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "spat5.viewer.mxo",
				"type" : "iLaX"
			}
, 			{
				"name" : "thru.maxpat",
				"bootpath" : "C74:/patchers/m4l/Pluggo for Live resources/patches",
				"type" : "JSON",
				"implicit" : 1
			}
 ],
		"autosave" : 0,
		"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
		"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
	}

}

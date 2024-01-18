{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 5,
			"revision" : 7,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 34.0, 97.0, 907.0, 644.0 ],
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
					"id" : "obj-21",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 4,
					"outlettype" : [ "", "dump", "bang", "" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 5,
							"revision" : 7,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 524.0, 97.0, 640.0, 575.0 ],
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
									"id" : "obj-22",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 3,
									"outlettype" : [ "", "int", "int" ],
									"patching_rect" : [ 420.0, 130.0, 81.0, 22.0 ],
									"text" : "change"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-19",
									"index" : 4,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 404.0, 509.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-18",
									"index" : 3,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 363.5, 509.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-17",
									"index" : 2,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 322.5, 509.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-16",
									"index" : 3,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "int" ],
									"patching_rect" : [ 420.0, 53.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-15",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 281.5, 411.0, 52.0, 22.0 ],
									"text" : "gate 1 0"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-14",
									"index" : 2,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 353.0, 53.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-13",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "bang" ],
									"patching_rect" : [ 314.5, 374.0, 48.0, 22.0 ],
									"text" : "del 100"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-12",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 401.5, 374.0, 35.0, 22.0 ],
									"text" : "/stop"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-10",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "bang", "bang" ],
									"patching_rect" : [ 314.5, 333.0, 106.0, 22.0 ],
									"text" : "t b b"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-9",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "bang", "" ],
									"patching_rect" : [ 314.5, 280.0, 72.0, 22.0 ],
									"text" : "sel 0"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-8",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "int", "int" ],
									"patching_rect" : [ 191.0, 222.0, 142.5, 22.0 ],
									"text" : "t i i"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-6",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 3,
									"outlettype" : [ "int", "dump", "bang" ],
									"patching_rect" : [ 281.5, 461.0, 101.0, 22.0 ],
									"text" : "t 48 dump b"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-5",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 191.0, 509.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-4",
									"maxclass" : "newobj",
									"numinlets" : 7,
									"numoutlets" : 2,
									"outlettype" : [ "int", "" ],
									"patching_rect" : [ 37.0, 333.0, 173.0, 22.0 ],
									"text" : "midiformat"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-3",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 37.0, 280.0, 173.0, 22.0 ],
									"text" : "0 0"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-2",
									"index" : 1,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 191.0, 53.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-1",
									"maxclass" : "newobj",
									"numinlets" : 3,
									"numoutlets" : 2,
									"outlettype" : [ "float", "float" ],
									"patching_rect" : [ 37.0, 130.0, 173.0, 22.0 ],
									"text" : "makenote 100 1000"
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-8", 0 ],
									"source" : [ "obj-1", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-12", 0 ],
									"source" : [ "obj-10", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-13", 0 ],
									"source" : [ "obj-10", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-19", 0 ],
									"source" : [ "obj-12", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-15", 1 ],
									"source" : [ "obj-13", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-13", 1 ],
									"midpoints" : [ 362.5, 267.0, 300.0, 267.0, 300.0, 362.0, 353.0, 362.0 ],
									"source" : [ "obj-14", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-6", 0 ],
									"source" : [ "obj-15", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-22", 0 ],
									"source" : [ "obj-16", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-1", 2 ],
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-15", 0 ],
									"midpoints" : [ 429.5, 318.0, 291.0, 318.0 ],
									"source" : [ "obj-22", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-6", 0 ],
									"midpoints" : [ 460.5, 447.0, 291.0, 447.0 ],
									"source" : [ "obj-22", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 0 ],
									"source" : [ "obj-3", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-5", 0 ],
									"source" : [ "obj-4", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-1", 0 ],
									"midpoints" : [ 291.0, 497.0, 24.0, 497.0, 24.0, 120.0, 46.5, 120.0 ],
									"source" : [ "obj-6", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-17", 0 ],
									"source" : [ "obj-6", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-18", 0 ],
									"source" : [ "obj-6", 2 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 1 ],
									"source" : [ "obj-8", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-9", 0 ],
									"source" : [ "obj-8", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 0 ],
									"source" : [ "obj-9", 0 ]
								}

							}
 ],
						"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
					}
,
					"patching_rect" : [ 532.5, 137.0, 133.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ],
						"globalpatchername" : "",
						"locked_bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"tags" : ""
					}
,
					"text" : "p midi"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-12",
					"linecount" : 4,
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 22.0, 471.0, 175.0, 60.0 ],
					"text" : "This coll displayed only the params selected to work with, useful for setting the indeces of scaling map"
				}

			}
, 			{
				"box" : 				{
					"color" : [ 0.639216, 0.458824, 0.070588, 1.0 ],
					"fontface" : 1,
					"id" : "obj-10",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "", "", "", "" ],
					"patching_rect" : [ 22.0, 541.0, 122.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 162.928571428571416, 100.0, 122.0, 22.0 ],
					"saved_object_attributes" : 					{
						"embed" : 0,
						"precision" : 6
					}
,
					"text" : "coll filtered_params"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-9",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 59.0, 231.5, 33.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.928571428571416, 70.0, 33.0, 22.0 ],
					"text" : "read"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-7",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 215.928571428571445, 392.0, 33.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.928571428571416, 130.0, 33.0, 22.0 ],
					"text" : "read"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-59",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 681.000000000000114, 541.0, 123.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 318.857142857142776, 8.0, 65.000000000000028, 20.0 ],
					"text" : "start/stop"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-58",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 104.0, 231.5, 35.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 78.928571428571416, 70.0, 39.0, 22.0 ],
					"text" : "clear"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-57",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 116.428571428571445, 392.0, 34.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 40.928571428571416, 130.0, 36.0, 22.0 ],
					"text" : "write"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-55",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 663.000000000000114, 534.0, 123.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 162.928571428571416, 10.0, 88.0, 20.0 ],
					"text" : "dump params"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-45",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 684.0, 1.5, 123.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 203.857142857142833, 130.0, 84.0, 20.0 ],
					"text" : "scaling map"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-39",
					"maxclass" : "textedit",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "", "int", "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 684.0, 23.5, 100.0, 50.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 289.857142857142833, 39.0, 94.0, 111.0 ],
					"text" : "1 2 3 4"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-27",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 701.0, 93.0, 83.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 212.39285714285711, 70.0, 72.535714285714334, 20.0 ],
					"text" : "preset int"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-26",
					"maxclass" : "number",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 532.5, 93.0, 50.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 162.928571428571416, 70.0, 50.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-2",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 646.5, 487.0, 135.0, 22.0 ],
					"text" : "udpsend localhost 5005"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-138",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 146.0, 231.5, 34.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 40.928571428571416, 70.0, 36.0, 22.0 ],
					"text" : "write"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-136",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 201.928571428571445, 231.5, 39.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 119.607142857142918, 70.0, 39.0, 22.0 ],
					"text" : "dump"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-120",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 161.0, 392.0, 35.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 78.928571428571416, 130.0, 39.0, 22.0 ],
					"text" : "clear"
				}

			}
, 			{
				"box" : 				{
					"color" : [ 0.870588, 0.415686, 0.062745, 1.0 ],
					"fontface" : 1,
					"id" : "obj-86",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 4,
					"outlettype" : [ "dictionary", "", "", "" ],
					"patching_rect" : [ 304.071428571428612, 471.0, 77.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.928571428571416, 100.0, 152.678571428571502, 22.0 ],
					"saved_object_attributes" : 					{
						"embed" : 0,
						"parameter_enable" : 0,
						"parameter_mappable" : 0
					}
,
					"text" : "dict storage"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-109",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 22.0, 373.0, 64.0, 22.0 ],
					"text" : "mc.dac~ 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-108",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "multichannelsignal" ],
					"patching_rect" : [ 22.0, 291.0, 92.0, 22.0 ],
					"text" : "mc.mixdown~ 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-107",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "multichannelsignal" ],
					"patching_rect" : [ 22.0, 198.5, 70.0, 22.0 ],
					"text" : "mc.pack~ 2"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-106",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 520.0, 23.5, 123.0, 20.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 214.928571428571416, 39.0, 72.928571428571416, 20.0 ],
					"text" : "preset rate"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-105",
					"maxclass" : "number",
					"minimum" : 1000,
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 589.5, 63.0, 50.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 162.928571428571416, 39.0, 50.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-103",
					"maxclass" : "toggle",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 646.5, 28.0, 24.0, 24.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 289.857142857142833, 6.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-99",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 5,
							"revision" : 7,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 338.0, 102.0, 747.0, 729.0 ],
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
									"id" : "obj-10",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 5,
									"outlettype" : [ "", "", "", "", "" ],
									"patching_rect" : [ 11.833333333333329, 262.0, 146.0, 22.0 ],
									"text" : "regexp \\\\/ @substitute %0"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-9",
									"linecount" : 2,
									"maxclass" : "newobj",
									"numinlets" : 5,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 11.833333333333329, 210.0, 146.0, 35.0 ],
									"text" : "combine year / month / day @padding 0 0 2 0 2"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-8",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 4,
									"outlettype" : [ "", "", "", "" ],
									"patching_rect" : [ 50.0, 171.0, 95.0, 22.0 ],
									"text" : "unjoin 3"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-30",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 4,
									"outlettype" : [ "", "", "", "" ],
									"patching_rect" : [ 162.0, 171.0, 138.0, 22.0 ],
									"text" : "unjoin 3"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-21",
									"linecount" : 2,
									"maxclass" : "newobj",
									"numinlets" : 5,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 162.0, 210.0, 138.0, 35.0 ],
									"text" : "combine hh : mm : sec @padding 2 0 2 0 2"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-13",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 5,
									"outlettype" : [ "", "", "", "", "" ],
									"patching_rect" : [ 162.0, 262.0, 146.0, 22.0 ],
									"text" : "regexp \\\\: @substitute %0"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-23",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 472.0, 461.0, 98.0, 22.0 ],
									"text" : "prepend /filepath"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-22",
									"linecount" : 2,
									"maxclass" : "comment",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 578.0, 275.0, 150.0, 33.0 ],
									"text" : "change here to save in a different location"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-20",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 402.0, 424.0, 35.0, 22.0 ],
									"text" : "/start"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-18",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "bang", "" ],
									"patching_rect" : [ 402.0, 389.0, 89.0, 22.0 ],
									"text" : "t b s"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-17",
									"index" : 2,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 472.0, 531.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-4",
									"linecount" : 2,
									"maxclass" : "newobj",
									"numinlets" : 9,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 402.0, 316.0, 169.0, 35.0 ],
									"text" : "combine . / snapshots / date - time . wav @triggers 4"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-7",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 50.0, 488.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-5",
									"maxclass" : "comment",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 361.0, 109.0, 150.0, 20.0 ],
									"text" : "param name, param value"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-3",
									"index" : 2,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 317.0, 109.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-2",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "", "float" ],
									"patching_rect" : [ 317.0, 171.0, 63.0, 22.0 ],
									"text" : "unpack s f"
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
									"patching_rect" : [ 50.0, 8.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-96",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 50.0, 389.0, 45.0, 22.0 ],
									"text" : "list.join"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-93",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 50.0, 424.0, 95.0, 22.0 ],
									"text" : "prepend replace"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-83",
									"linecount" : 2,
									"maxclass" : "newobj",
									"numinlets" : 5,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 50.0, 316.0, 207.0, 35.0 ],
									"text" : "combine date - time :: param_name @triggers 4"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-76",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 50.0, 73.0, 61.0, 22.0 ],
									"text" : "date, time"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-72",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 50.0, 135.0, 55.0, 22.0 ],
									"text" : "$3 $1 $2"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-66",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 3,
									"outlettype" : [ "list", "list", "int" ],
									"patching_rect" : [ 50.0, 107.0, 243.0, 22.0 ],
									"text" : "date"
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-76", 0 ],
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 4 ],
									"midpoints" : [ 21.333333333333329, 303.5, 486.5, 303.5 ],
									"order" : 0,
									"source" : [ "obj-10", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-83", 0 ],
									"order" : 1,
									"source" : [ "obj-10", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 6 ],
									"midpoints" : [ 171.5, 294.5, 524.0, 294.5 ],
									"order" : 0,
									"source" : [ "obj-13", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-83", 2 ],
									"order" : 1,
									"source" : [ "obj-13", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-20", 0 ],
									"source" : [ "obj-18", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-23", 0 ],
									"source" : [ "obj-18", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-83", 4 ],
									"midpoints" : [ 326.5, 300.0, 247.5, 300.0 ],
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-96", 1 ],
									"midpoints" : [ 370.5, 374.0, 85.5, 374.0 ],
									"source" : [ "obj-2", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-17", 0 ],
									"source" : [ "obj-20", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-13", 0 ],
									"source" : [ "obj-21", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-17", 0 ],
									"source" : [ "obj-23", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-2", 0 ],
									"source" : [ "obj-3", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-21", 4 ],
									"source" : [ "obj-30", 2 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-21", 2 ],
									"source" : [ "obj-30", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-21", 0 ],
									"source" : [ "obj-30", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-18", 0 ],
									"source" : [ "obj-4", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-30", 0 ],
									"source" : [ "obj-66", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-72", 0 ],
									"source" : [ "obj-66", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-8", 0 ],
									"source" : [ "obj-72", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-66", 0 ],
									"source" : [ "obj-76", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-9", 4 ],
									"source" : [ "obj-8", 2 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-9", 2 ],
									"source" : [ "obj-8", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-9", 0 ],
									"source" : [ "obj-8", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-96", 0 ],
									"source" : [ "obj-83", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 0 ],
									"source" : [ "obj-9", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-7", 0 ],
									"source" : [ "obj-93", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-93", 0 ],
									"source" : [ "obj-96", 0 ]
								}

							}
 ],
						"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
					}
,
					"patching_rect" : [ 304.071428571428612, 400.0, 59.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ],
						"globalpatchername" : "",
						"locked_bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"tags" : ""
					}
,
					"text" : "p storage"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-60",
					"maxclass" : "newobj",
					"numinlets" : 4,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 5,
							"revision" : 7,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 286.0, 97.0, 810.0, 723.0 ],
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
									"id" : "obj-7",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 4,
									"outlettype" : [ "", "", "", "" ],
									"patching_rect" : [ 472.5, 307.0, 113.0, 22.0 ],
									"saved_object_attributes" : 									{
										"embed" : 0,
										"precision" : 6
									}
,
									"text" : "coll filtered_params"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-1",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "list" ],
									"patching_rect" : [ 472.5, 271.0, 66.0, 22.0 ],
									"text" : "listfunnel 1"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-17",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 431.5, 464.0, 59.0, 22.0 ],
									"text" : "route text"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-16",
									"index" : 2,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 310.0, 24.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-15",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 252.0, 78.0, 77.0, 22.0 ],
									"text" : "list.join"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-14",
									"index" : 2,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 197.5, 679.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-13",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 65.5, 634.0, 151.0, 22.0 ],
									"text" : "t l l"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-8",
									"linecount" : 4,
									"maxclass" : "comment",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 541.0, 438.0, 188.0, 60.0 ],
									"text" : "scale map\n<index number (1-based)>\n<new min>\n<new max>"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-6",
									"index" : 4,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 431.5, 410.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-32",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 193.5, 503.0, 257.0, 22.0 ],
									"saved_object_attributes" : 									{
										"filename" : "param_scaler.js",
										"parameter_enable" : 0
									}
,
									"text" : "js param_scaler.js"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-28",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 252.0, 114.0, 77.0, 22.0 ],
									"text" : "route symbol"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-27",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 65.5, 679.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-26",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 65.5, 589.0, 151.0, 22.0 ],
									"text" : "list.iter 2 @zlmaxsize 4096"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-23",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 65.5, 545.0, 147.0, 22.0 ],
									"text" : "list.lace @zlmaxsize 4096"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-22",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 3,
									"outlettype" : [ "", "", "" ],
									"patching_rect" : [ 252.0, 232.0, 40.0, 22.0 ],
									"text" : "t l l l"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-12",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "float" ],
									"patching_rect" : [ 263.0, 418.0, 53.0, 22.0 ],
									"text" : "* 0.0001"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-11",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "int" ],
									"patching_rect" : [ 263.0, 374.0, 86.0, 22.0 ],
									"text" : "random 10000"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-5",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 3,
									"outlettype" : [ "bang", "bang", "int" ],
									"patching_rect" : [ 263.0, 341.0, 40.0, 22.0 ],
									"text" : "uzi"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-4",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "int", "int" ],
									"patching_rect" : [ 263.0, 307.0, 85.5, 22.0 ],
									"text" : "t i i"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-3",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 193.5, 464.0, 155.0, 22.0 ],
									"text" : "list.group @zlmaxsize 2048"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-2",
									"linecount" : 2,
									"maxclass" : "comment",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 61.0, 156.5, 119.0, 33.0 ],
									"text" : "length of random numbers to generate"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-56",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 263.0, 271.0, 141.0, 22.0 ],
									"text" : "list.len @zlmaxsize 2048"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-55",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 252.0, 152.0, 29.5, 22.0 ],
									"text" : "$1"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-53",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"patching_rect" : [ 252.0, 192.0, 169.0, 22.0 ],
									"text" : "list.group -1 @zlmaxsize 2048"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-58",
									"index" : 1,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 252.0, 24.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-59",
									"index" : 3,
									"maxclass" : "inlet",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 391.0, 24.0, 30.0, 30.0 ]
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-7", 0 ],
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-12", 0 ],
									"source" : [ "obj-11", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"midpoints" : [ 272.5, 451.5, 203.0, 451.5 ],
									"source" : [ "obj-12", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-14", 0 ],
									"source" : [ "obj-13", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-27", 0 ],
									"source" : [ "obj-13", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-28", 0 ],
									"source" : [ "obj-15", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-15", 1 ],
									"source" : [ "obj-16", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-32", 1 ],
									"source" : [ "obj-17", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-1", 0 ],
									"midpoints" : [ 282.5, 262.0, 482.0, 262.0 ],
									"source" : [ "obj-22", 2 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-23", 0 ],
									"midpoints" : [ 261.5, 269.0, 75.0, 269.0 ],
									"source" : [ "obj-22", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-56", 0 ],
									"source" : [ "obj-22", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-26", 0 ],
									"source" : [ "obj-23", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-13", 0 ],
									"source" : [ "obj-26", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-55", 0 ],
									"source" : [ "obj-28", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-32", 0 ],
									"source" : [ "obj-3", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-23", 1 ],
									"source" : [ "obj-32", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 1 ],
									"midpoints" : [ 339.0, 361.0, 361.0, 361.0, 361.0, 451.0, 339.0, 451.0 ],
									"source" : [ "obj-4", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-5", 0 ],
									"source" : [ "obj-4", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-11", 0 ],
									"source" : [ "obj-5", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-22", 0 ],
									"source" : [ "obj-53", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-53", 0 ],
									"source" : [ "obj-55", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 0 ],
									"source" : [ "obj-56", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-15", 0 ],
									"source" : [ "obj-58", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-53", 0 ],
									"midpoints" : [ 400.5, 185.5, 261.5, 185.5 ],
									"source" : [ "obj-59", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-17", 0 ],
									"source" : [ "obj-6", 0 ]
								}

							}
 ],
						"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
					}
,
					"patching_rect" : [ 257.071428571428612, 351.0, 106.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ],
						"globalpatchername" : "",
						"locked_bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
						"tags" : ""
					}
,
					"text" : "p random_params"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-43",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "list" ],
					"patching_rect" : [ 257.071428571428612, 231.5, 66.0, 22.0 ],
					"text" : "listfunnel 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-42",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 257.071428571428612, 198.5, 169.0, 22.0 ],
					"text" : "list.group -1 @zlmaxsize 2048"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-41",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 410.60714285714289, 137.0, 48.0, 22.0 ],
					"text" : "del 500"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-24",
					"linecount" : 4,
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 543.60714285714289, 285.0, 175.0, 60.0 ],
					"text" : "coll:\n- add a 0 at the end of the params you want to exclude it from render!!!"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 1,
					"id" : "obj-17",
					"linecount" : 2,
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 446.60714285714289, 32.0, 62.0, 33.0 ],
					"text" : "dump params"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-15",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 410.60714285714289, 30.0, 24.0, 24.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 134.60714285714289, 8.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-11",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "bang", "params", "clear" ],
					"patching_rect" : [ 410.60714285714289, 93.0, 95.0, 22.0 ],
					"text" : "t b params clear"
				}

			}
, 			{
				"box" : 				{
					"coll_data" : 					{
						"count" : 155,
						"data" : [ 							{
								"key" : 1,
								"value" : [ "Cutoff", 0 ]
							}
, 							{
								"key" : 2,
								"value" : [ "Resonance", 0 ]
							}
, 							{
								"key" : 3,
								"value" : [ "Output", 0 ]
							}
, 							{
								"key" : 4,
								"value" : [ "MASTER TUNE ADJ", 0 ]
							}
, 							{
								"key" : 5,
								"value" : [ "ALGORITHM", 0 ]
							}
, 							{
								"key" : 6,
								"value" : [ "FEEDBACK" ]
							}
, 							{
								"key" : 7,
								"value" : [ "OSC KEY SYNC" ]
							}
, 							{
								"key" : 8,
								"value" : [ "LFO SPEED" ]
							}
, 							{
								"key" : 9,
								"value" : [ "LFO DELAY" ]
							}
, 							{
								"key" : 10,
								"value" : [ "LFO PM DEPTH" ]
							}
, 							{
								"key" : 11,
								"value" : [ "LFO AM DEPTH" ]
							}
, 							{
								"key" : 12,
								"value" : [ "LFO KEY SYNC" ]
							}
, 							{
								"key" : 13,
								"value" : [ "LFO WAVE" ]
							}
, 							{
								"key" : 14,
								"value" : [ "TRANSPOSE", 0 ]
							}
, 							{
								"key" : 15,
								"value" : [ "P MODE SENS." ]
							}
, 							{
								"key" : 16,
								"value" : [ "PITCH EG RATE 1" ]
							}
, 							{
								"key" : 17,
								"value" : [ "PITCH EG RATE 2" ]
							}
, 							{
								"key" : 18,
								"value" : [ "PITCH EG RATE 3" ]
							}
, 							{
								"key" : 19,
								"value" : [ "PITCH EG RATE 4" ]
							}
, 							{
								"key" : 20,
								"value" : [ "PITCH EG LEVEL 1" ]
							}
, 							{
								"key" : 21,
								"value" : [ "PITCH EG LEVEL 2" ]
							}
, 							{
								"key" : 22,
								"value" : [ "PITCH EG LEVEL 3" ]
							}
, 							{
								"key" : 23,
								"value" : [ "PITCH EG LEVEL 4" ]
							}
, 							{
								"key" : 24,
								"value" : [ "OP1 EG RATE 1" ]
							}
, 							{
								"key" : 25,
								"value" : [ "OP1 EG RATE 2" ]
							}
, 							{
								"key" : 26,
								"value" : [ "OP1 EG RATE 3" ]
							}
, 							{
								"key" : 27,
								"value" : [ "OP1 EG RATE 4" ]
							}
, 							{
								"key" : 28,
								"value" : [ "OP1 EG LEVEL 1" ]
							}
, 							{
								"key" : 29,
								"value" : [ "OP1 EG LEVEL 2" ]
							}
, 							{
								"key" : 30,
								"value" : [ "OP1 EG LEVEL 3" ]
							}
, 							{
								"key" : 31,
								"value" : [ "OP1 EG LEVEL 4" ]
							}
, 							{
								"key" : 32,
								"value" : [ "OP1 OUTPUT LEVEL" ]
							}
, 							{
								"key" : 33,
								"value" : [ "OP1 MODE", 0 ]
							}
, 							{
								"key" : 34,
								"value" : [ "OP1 F COARSE" ]
							}
, 							{
								"key" : 35,
								"value" : [ "OP1 F FINE" ]
							}
, 							{
								"key" : 36,
								"value" : [ "OP1 OSC DETUNE" ]
							}
, 							{
								"key" : 37,
								"value" : [ "OP1 BREAK POINT", 0 ]
							}
, 							{
								"key" : 38,
								"value" : [ "OP1 L SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 39,
								"value" : [ "OP1 R SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 40,
								"value" : [ "OP1 L KEY SCALE", 0 ]
							}
, 							{
								"key" : 41,
								"value" : [ "OP1 R KEY SCALE", 0 ]
							}
, 							{
								"key" : 42,
								"value" : [ "OP1 RATE SCALING", 0 ]
							}
, 							{
								"key" : 43,
								"value" : [ "OP1 A MOD SENS.", 0 ]
							}
, 							{
								"key" : 44,
								"value" : [ "OP1 KEY VELOCITY", 0 ]
							}
, 							{
								"key" : 45,
								"value" : [ "OP1 SWITCH", 0 ]
							}
, 							{
								"key" : 46,
								"value" : [ "OP2 EG RATE 1" ]
							}
, 							{
								"key" : 47,
								"value" : [ "OP2 EG RATE 2" ]
							}
, 							{
								"key" : 48,
								"value" : [ "OP2 EG RATE 3" ]
							}
, 							{
								"key" : 49,
								"value" : [ "OP2 EG RATE 4" ]
							}
, 							{
								"key" : 50,
								"value" : [ "OP2 EG LEVEL 1" ]
							}
, 							{
								"key" : 51,
								"value" : [ "OP2 EG LEVEL 2" ]
							}
, 							{
								"key" : 52,
								"value" : [ "OP2 EG LEVEL 3" ]
							}
, 							{
								"key" : 53,
								"value" : [ "OP2 EG LEVEL 4" ]
							}
, 							{
								"key" : 54,
								"value" : [ "OP2 OUTPUT LEVEL" ]
							}
, 							{
								"key" : 55,
								"value" : [ "OP2 MODE", 0 ]
							}
, 							{
								"key" : 56,
								"value" : [ "OP2 F COARSE" ]
							}
, 							{
								"key" : 57,
								"value" : [ "OP2 F FINE" ]
							}
, 							{
								"key" : 58,
								"value" : [ "OP2 OSC DETUNE" ]
							}
, 							{
								"key" : 59,
								"value" : [ "OP2 BREAK POINT", 0 ]
							}
, 							{
								"key" : 60,
								"value" : [ "OP2 L SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 61,
								"value" : [ "OP2 R SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 62,
								"value" : [ "OP2 L KEY SCALE", 0 ]
							}
, 							{
								"key" : 63,
								"value" : [ "OP2 R KEY SCALE", 0 ]
							}
, 							{
								"key" : 64,
								"value" : [ "OP2 RATE SCALING", 0 ]
							}
, 							{
								"key" : 65,
								"value" : [ "OP2 A MOD SENS.", 0 ]
							}
, 							{
								"key" : 66,
								"value" : [ "OP2 KEY VELOCITY", 0 ]
							}
, 							{
								"key" : 67,
								"value" : [ "OP2 SWITCH", 0 ]
							}
, 							{
								"key" : 68,
								"value" : [ "OP3 EG RATE 1" ]
							}
, 							{
								"key" : 69,
								"value" : [ "OP3 EG RATE 2" ]
							}
, 							{
								"key" : 70,
								"value" : [ "OP3 EG RATE 3" ]
							}
, 							{
								"key" : 71,
								"value" : [ "OP3 EG RATE 4" ]
							}
, 							{
								"key" : 72,
								"value" : [ "OP3 EG LEVEL 1" ]
							}
, 							{
								"key" : 73,
								"value" : [ "OP3 EG LEVEL 2" ]
							}
, 							{
								"key" : 74,
								"value" : [ "OP3 EG LEVEL 3" ]
							}
, 							{
								"key" : 75,
								"value" : [ "OP3 EG LEVEL 4" ]
							}
, 							{
								"key" : 76,
								"value" : [ "OP3 OUTPUT LEVEL" ]
							}
, 							{
								"key" : 77,
								"value" : [ "OP3 MODE", 0 ]
							}
, 							{
								"key" : 78,
								"value" : [ "OP3 F COARSE" ]
							}
, 							{
								"key" : 79,
								"value" : [ "OP3 F FINE" ]
							}
, 							{
								"key" : 80,
								"value" : [ "OP3 OSC DETUNE" ]
							}
, 							{
								"key" : 81,
								"value" : [ "OP3 BREAK POINT", 0 ]
							}
, 							{
								"key" : 82,
								"value" : [ "OP3 L SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 83,
								"value" : [ "OP3 R SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 84,
								"value" : [ "OP3 L KEY SCALE", 0 ]
							}
, 							{
								"key" : 85,
								"value" : [ "OP3 R KEY SCALE", 0 ]
							}
, 							{
								"key" : 86,
								"value" : [ "OP3 RATE SCALING", 0 ]
							}
, 							{
								"key" : 87,
								"value" : [ "OP3 A MOD SENS.", 0 ]
							}
, 							{
								"key" : 88,
								"value" : [ "OP3 KEY VELOCITY", 0 ]
							}
, 							{
								"key" : 89,
								"value" : [ "OP3 SWITCH", 0 ]
							}
, 							{
								"key" : 90,
								"value" : [ "OP4 EG RATE 1" ]
							}
, 							{
								"key" : 91,
								"value" : [ "OP4 EG RATE 2" ]
							}
, 							{
								"key" : 92,
								"value" : [ "OP4 EG RATE 3" ]
							}
, 							{
								"key" : 93,
								"value" : [ "OP4 EG RATE 4" ]
							}
, 							{
								"key" : 94,
								"value" : [ "OP4 EG LEVEL 1" ]
							}
, 							{
								"key" : 95,
								"value" : [ "OP4 EG LEVEL 2" ]
							}
, 							{
								"key" : 96,
								"value" : [ "OP4 EG LEVEL 3" ]
							}
, 							{
								"key" : 97,
								"value" : [ "OP4 EG LEVEL 4" ]
							}
, 							{
								"key" : 98,
								"value" : [ "OP4 OUTPUT LEVEL" ]
							}
, 							{
								"key" : 99,
								"value" : [ "OP4 MODE", 0 ]
							}
, 							{
								"key" : 100,
								"value" : [ "OP4 F COARSE" ]
							}
, 							{
								"key" : 101,
								"value" : [ "OP4 F FINE" ]
							}
, 							{
								"key" : 102,
								"value" : [ "OP4 OSC DETUNE" ]
							}
, 							{
								"key" : 103,
								"value" : [ "OP4 BREAK POINT", 0 ]
							}
, 							{
								"key" : 104,
								"value" : [ "OP4 L SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 105,
								"value" : [ "OP4 R SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 106,
								"value" : [ "OP4 L KEY SCALE", 0 ]
							}
, 							{
								"key" : 107,
								"value" : [ "OP4 R KEY SCALE", 0 ]
							}
, 							{
								"key" : 108,
								"value" : [ "OP4 RATE SCALING", 0 ]
							}
, 							{
								"key" : 109,
								"value" : [ "OP4 A MOD SENS.", 0 ]
							}
, 							{
								"key" : 110,
								"value" : [ "OP4 KEY VELOCITY", 0 ]
							}
, 							{
								"key" : 111,
								"value" : [ "OP4 SWITCH", 0 ]
							}
, 							{
								"key" : 112,
								"value" : [ "OP5 EG RATE 1" ]
							}
, 							{
								"key" : 113,
								"value" : [ "OP5 EG RATE 2" ]
							}
, 							{
								"key" : 114,
								"value" : [ "OP5 EG RATE 3" ]
							}
, 							{
								"key" : 115,
								"value" : [ "OP5 EG RATE 4" ]
							}
, 							{
								"key" : 116,
								"value" : [ "OP5 EG LEVEL 1" ]
							}
, 							{
								"key" : 117,
								"value" : [ "OP5 EG LEVEL 2" ]
							}
, 							{
								"key" : 118,
								"value" : [ "OP5 EG LEVEL 3" ]
							}
, 							{
								"key" : 119,
								"value" : [ "OP5 EG LEVEL 4" ]
							}
, 							{
								"key" : 120,
								"value" : [ "OP5 OUTPUT LEVEL" ]
							}
, 							{
								"key" : 121,
								"value" : [ "OP5 MODE", 0 ]
							}
, 							{
								"key" : 122,
								"value" : [ "OP5 F COARSE" ]
							}
, 							{
								"key" : 123,
								"value" : [ "OP5 F FINE" ]
							}
, 							{
								"key" : 124,
								"value" : [ "OP5 OSC DETUNE" ]
							}
, 							{
								"key" : 125,
								"value" : [ "OP5 BREAK POINT", 0 ]
							}
, 							{
								"key" : 126,
								"value" : [ "OP5 L SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 127,
								"value" : [ "OP5 R SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 128,
								"value" : [ "OP5 L KEY SCALE", 0 ]
							}
, 							{
								"key" : 129,
								"value" : [ "OP5 R KEY SCALE", 0 ]
							}
, 							{
								"key" : 130,
								"value" : [ "OP5 RATE SCALING", 0 ]
							}
, 							{
								"key" : 131,
								"value" : [ "OP5 A MOD SENS.", 0 ]
							}
, 							{
								"key" : 132,
								"value" : [ "OP5 KEY VELOCITY", 0 ]
							}
, 							{
								"key" : 133,
								"value" : [ "OP5 SWITCH", 0 ]
							}
, 							{
								"key" : 134,
								"value" : [ "OP6 EG RATE 1" ]
							}
, 							{
								"key" : 135,
								"value" : [ "OP6 EG RATE 2" ]
							}
, 							{
								"key" : 136,
								"value" : [ "OP6 EG RATE 3" ]
							}
, 							{
								"key" : 137,
								"value" : [ "OP6 EG RATE 4" ]
							}
, 							{
								"key" : 138,
								"value" : [ "OP6 EG LEVEL 1" ]
							}
, 							{
								"key" : 139,
								"value" : [ "OP6 EG LEVEL 2" ]
							}
, 							{
								"key" : 140,
								"value" : [ "OP6 EG LEVEL 3" ]
							}
, 							{
								"key" : 141,
								"value" : [ "OP6 EG LEVEL 4" ]
							}
, 							{
								"key" : 142,
								"value" : [ "OP6 OUTPUT LEVEL" ]
							}
, 							{
								"key" : 143,
								"value" : [ "OP6 MODE", 0 ]
							}
, 							{
								"key" : 144,
								"value" : [ "OP6 F COARSE" ]
							}
, 							{
								"key" : 145,
								"value" : [ "OP6 F FINE" ]
							}
, 							{
								"key" : 146,
								"value" : [ "OP6 OSC DETUNE" ]
							}
, 							{
								"key" : 147,
								"value" : [ "OP6 BREAK POINT", 0 ]
							}
, 							{
								"key" : 148,
								"value" : [ "OP6 L SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 149,
								"value" : [ "OP6 R SCALE DEPTH", 0 ]
							}
, 							{
								"key" : 150,
								"value" : [ "OP6 L KEY SCALE", 0 ]
							}
, 							{
								"key" : 151,
								"value" : [ "OP6 R KEY SCALE", 0 ]
							}
, 							{
								"key" : 152,
								"value" : [ "OP6 RATE SCALING", 0 ]
							}
, 							{
								"key" : 153,
								"value" : [ "OP6 A MOD SENS.", 0 ]
							}
, 							{
								"key" : 154,
								"value" : [ "OP6 KEY VELOCITY", 0 ]
							}
, 							{
								"key" : 155,
								"value" : [ "OP6 SWITCH", 0 ]
							}
 ]
					}
,
					"color" : [ 0.862745, 0.741176, 0.137255, 1.0 ],
					"fontface" : 1,
					"id" : "obj-5",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "", "", "", "" ],
					"patching_rect" : [ 257.071428571428612, 291.0, 274.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.928571428571416, 39.0, 152.678571428571473, 22.0 ],
					"saved_object_attributes" : 					{
						"embed" : 1,
						"precision" : 6
					}
,
					"text" : "coll instrument_params"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 205.928571428571445, 30.0, 31.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 5.928571428571416, 9.0, 33.0, 22.0 ],
					"text" : "plug"
				}

			}
, 			{
				"box" : 				{
					"autosave" : 1,
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"color" : [ 0.439216, 0.74902, 0.254902, 1.0 ],
					"fontface" : 1,
					"id" : "obj-1",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 8,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal", "signal", "", "list", "int", "", "", "" ],
					"patching_rect" : [ 205.928571428571445, 159.0, 198.0, 22.0 ],
					"presentation" : 1,
					"presentation_rect" : [ 40.928571428571416, 9.0, 90.0, 22.0 ],
					"save" : [ "#N", "vst~", "loaduniqueid", 0, ";" ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_invisible" : 1,
							"parameter_longname" : "vst~",
							"parameter_shortname" : "vst~",
							"parameter_type" : 3
						}

					}
,
					"saved_object_attributes" : 					{
						"parameter_enable" : 1,
						"parameter_mappable" : 0,
						"prefer" : "AudioUnit"
					}
,
					"snapshot" : 					{
						"filetype" : "C74Snapshot",
						"version" : 2,
						"minorversion" : 0,
						"name" : "snapshotlist",
						"origin" : "vst~",
						"type" : "list",
						"subtype" : "Undefined",
						"embed" : 1,
						"snapshot" : 						{
							"pluginname" : "Dexed.component",
							"plugindisplayname" : "Dexed",
							"pluginsavedname" : "/Library/Audio/Plug-Ins/Components/Dexed.component",
							"pluginsaveduniqueid" : 0,
							"version" : 1,
							"isbank" : 0,
							"isbase64" : 1,
							"blob" : "7560.hAGaoMGcv.C1AHv.DTfAGfPBJr.DQHwDTvUag4VclE1XzUmbkIGUjEFcgwUYrUVak4Fcs3VXsU1UyUmXzkGbkckckI2bo8laTQWdvU1WP7fZ0MVYPwVcmklaSQWXzUFUtEVakIAQGMkPOEAAjC..............aB....yO.B......w.........fL+.H......LyO........z7Cf......PM+.H......XyO.B......23SsBXI....N.........jC.......fAe........X.H+.H.....FDB.......fAh7C......XvH9rca2B..FPxO.B....fAk7Cf.....XfI+.H.....FbxO.B....fAn7S.J0O..XfO+DfR8C..F7yOAnT+..fA.8S.J0O..XPP+Ti.VB..FHjON6sX..fAC4S+pU...X.Q+.H.....FTzO.B....fAF8SalSB..XvQ........FzE.......fAd8Cf.....XvW........F.VODDBB..fAgA.......XfX+.......FLF.......fAjA.......XPY........FXF.......fA7A.......XPe........F3G.......fA+A.......X.f+.H.....FDnOApT+..fAB9SI9UK..Xvf9zuZE...FP3O.B....fAE9S.J0O..Xvl+.H.....FvI.......fAcB.......Xfm+.H.....F7I.......fAfB.......XPn........FH5O......fAiB.......X.o........FnK.......fA6B.......X.u........FzK.......fA9B.......Xvu........F.7O.B....fAA6yFlnL..Xfv+The0B..FLrO8qVA..fAY+Cf.....Xf19Lti4...Fr8O.B....fAbC.......XP2........F38O.B....fAeC.......X.38PXHH...FDN.......fAh+C......X.9........FjO.......fA5C.......Xv9........FvO.......fA8C.......Xf+........F7O.......vA.7Cf.....bP.9XfcyC..GbwOk3Ws..vAX3S+pU...bPF+.H.....GngOsaNI..vAa7Cf.....b.G........GzA.......vAd7Cf.....bvG........G.B.......PuwC.......zq7+.......8NO.......PuzC.......za8........8ZO.......Pu2C.......zK9........8lO.......Pu5C.......3KD+.H.....9FQON6sX..fuR7SI9UK..36D9zuZE...9RwO.B....fuU3S6lSB..3qE+.H.....9dA.......fuX........3aF+.H.....99B.......fuvzCggf...3aL........9JyO......fuy........3KM........9VC.......fu1........36M........9hC.......fuNA.......36S........9B0O.B....fuQ0CjN6M..3qT+The0B..9NkOnq6K..fuT8Cf.....3aU9fttu...9Z0O.B....fuWA.......3aa........951O.B....fuuA.......3Kb........9FG.......fux8C......36b........9RG.......fu0A.......3qc........9xH.......fuMB.......3qi........99H.......fuP9Cf..PzLzPTxDsCODELV8TczAWczIAQkgGYP.fDgUWa08TDWDrUCISH3dA..vyO30FafXWYxMWZu4VOhDiKvHBHk41XuQVZtcVOhTEUF0BNh7iOfvCYkgWYjMEcgQWYfLVcz8lYl0iHw3BLh.hbkM2a8HBLt.iHfbVXo4VOhDiKvHBHiUmbxUlazAkbuclbg0VOh.iHfz1at8VSuQVY8HBLh.RYtcVZtUFU4AWY8HRLh.RagMGckIGU04VY8HBLh.xavM0coQ2Xn0iHwDSLwDSLh.BcxElayA2ayUVLxDzbSMVXrUVOhDiHfzFbkUjagIFakQVOh.iHfzFbkAUZzMFZBUlajIUXtcVY8HhLzHBH2gVYkwVSuQVOh.CHv.BLf.iHfX1auQWSuQVOh.CHv.BLf.iHfHlbkEFcn0zaj0iHv.BLf.CHvHBHgYFckIGcuU2Xn0zaj0iHv.BLf.CHvHhO7PVY3UFYBw1ahAhXgMWY1PiNyk2bkgWOhPSLvPiK18DQtjjKB4xQtP0RoACdX4hKt3hKt3hKy3hcX4hKlIjKEkGVzwjQt3hKt3hKt3hStvjQA4hdt.0cLw1RoEjKt3hKt3hKlMjKoEjKt7jKTwTZ2gGVt3hKt3hKt3xLtXGVD4BTF4RQ4gEdLYjKt3hKt3hKt3jKLYjKtfEQJcGSwfkXA4hKt3hKt3hYC4RZI4hKo0TLXkVRowDdHk2QOwjPt3hKPwDVLUEVzDjTP0VQVoEczHjTL8lKHkVUEQkKDMjKt3hKNgDTEUjK1QkTJY2cXI1aE4Bdt3hKtXVPAoUTt3xctolPlgDaXgVPPoDNtnlPHclcQQjK10zStY2RocWQW4hY4YkKL4hXDwjQA4hXCgjY5E0Uj8VQtPTP1gkPt3RPXEETtHiYoITcLwFVtDjcIkVP1MDVmYFVDQjYXgVRrgELDkFS3MicCcFSBQjKtDzPLUDUUI0ZTEkYtHDRlwDaKECUvfkYMYjKz3hKt3haCETZUYmToQCZHEVSwbUZA4hKt3hKtjWPlM0QDMjUIU0TWkFLD4hKt3hKt3hYhIlbEQzPlUjS2nGLX0TPt3hKt3hKtvTQE8TRtbDVmMzSi0jUS4hKt3hKt3hKoY1cTIDRrMkY1IzSoUUQt3hKt3hKtXlRtvjQtbDVUcUZMYjK54BTWE0M1gjKt3hK24hYPsVQFM1bUYjV3EEahkVVRYzaLYjTHEjcI4BQ1MjcQYFUD4hcX0lZQgTZiQDTtHlPt3xMtHlKPMTPtvjQSkFN3gEVAYjKs4hKt7jKG4hXI4hKoMlTFcFSwDkKAYWRtPjcCMCT1gEQtXGVroVPIk1YDIkKhIjKtbiKN4xLDIjKLYzTogCdXgUPF4Rat3hKOY1Pt3BRt3BU3.yU2fTZLgGR4cjSTIjKt3hKPgkKEIUPIAyTHEjPHYlK3gkcD4hQjgCQt3hco0jKDYWTLwDaG4xMvfDR1cGVFEjKtnmK1gzP1UDQOkkKtTVPRYzYLwVTt3hKt3hKt3RXhcGVB4BTUgGRlITZYQjKt31PtrlK1IjK2nFQtHmZKAkc1gkQA4hK5YlKtLjbBMzSQ4hKJQycFUFSrEkKt3xSt3hKtj1X2gkPtX1UCgSQOgGRowDdHY1PnQjPt3hZAMzPmwlX0AiUXYFUCgjXUs1SXoGdXkVPt3hYt3hKCA0ctvzaPQEUukFQpwjUW4hKtfjKHEjK1XWTVQjK1U0bxE0Ro0jQt3hK3gkKLYlKPwDat3BUq8DVyfGVoEjKtXlKt3xP14hKG8FTtX0aoQjZLY0Ut3hKH4BRA4xPPEkUDQjKVMmbQsTZMYjKt3BdX4BSl4BTLwlKA4hKt3hKlwDdHkFSCYFTF4hat3BR14xTmk0UZoWQrIlYtHzUt3hKDUFSwfUZA4hKt.kKt.UStPkPtXVTt3RTEEVSwfkKt3hKt3hKT4xLp4hKyHjKOgkPWkVSF4hKt3hKt3RQtjVRt3hKt3hKlwTLXkVPt3hKt3hKtgjKT4BSrwjKpYFQl0TLX4hYA4RQt3hStfTQtjFMB4hXXI0Uo0jQt3hKt3hKt3hKoUDTAkVSwfUZIkFS3gTdtrjXA4xSt.EQLwTQgUWSvLlbAg2R0Y2ZSUVV5ITZAEiTtH1PtDlKPIlK2LTPtXFZGkET3gkVuUjK44hKt3BQ24RZI4hK4byZQwDSFg0SA4BStLSPtjkKtDEQt3hRjoVPIk1aqYkKLMjKt3BTXcESr4RPpk2UFMmcXY1bE4BZtXFRtnlQtfTRt3hayDkQpwDaVoUP1wjKt3hKIwzcXIjKP4zTAUTUwwTZLgGUPEjXtjFRoclPF8TRDgzQUwVXwrFaiIVSwTzRyXGVYcWQt7jKt3BQXUjKv.0TtHDM1IjXyTkUZEjcC4hKtDjUQ4hTF4hKV4DSpkTZqASTtbiKt3BTlsjKls1RtX1ZCczX3gUVmUjKO4hKtPzLC4xYI4hKnETLFAGSFcjTAY2PtLiKAYWPtfEQ2HCVJIlKKkVPVYkK23hKNAkKh4BSF4hKLECVo0TLIgGUosjS2.UPtvjQtnWP1QUPiUDREACQHUUPEgTdtgGRQwTLXkVPlcjKX4hKl0jKKIjK1wTTHgVQo0TLX4xLA4RTt3BVBwDat3hankDUybGVo0jQtXlKt3hKtXjPokjKt.iaRkTVLECVo0DaG4BSt3hKMY1StvjUMEER3UTZMECVtLSPtzjKt.kPHYjKo8FZIQ0M2gUZMYjKl4hKt3hKDITZAYGVo0TLTkFN30DdHkmKMQjKt3BUEIDS1oVTOkTUYUSP3oTb1ACVXwjQJ4hK1gkKt3hKt3BTN4hKl4hKLYDRoclPt3BSF4hKt3hKtn1PtjVP1wTZMgGVt4hKtfVPt3hKt3hKz3hcX4hK1gUaLYjRt3hcX4hKt3hKt.kStvDat3BSVsTZmIjKtvjQt3hKt3hKpMjKokjYFkVS3gkaLESTt3hKt3hKt3BMtXGVBomcXkVSFoDdHkFS3cSPBQ0MpcjPhEjQEQidP8TUqMEUUoFUSMmcCckYoM0RMYjKt3hKt3hKG4RZUAURo0TLXICSwfUZA4hKt3hKtXWPlckKtXmPOIVTN4zb5gkKt3hKt3hKF4BSVEDaLECVocVdXkVSF4hKt3hKt3hKtPVPt3xR2XWQwLidRkVPt3hKt3hK1EjcXUDV3gUZMYUSo0TLX4hKt3hKt3hStLSQt3BSFcTZMwFS3gTZLQzMlsjKy.0RvXVPU4VUsElZUwlXl4BdL4BUUMTbHkGVt3hYC4hKt3hSAYGUH4hKCcUU3oDLLYjKtLiKt3hKtPjKLYTPtn1cUglbn4TZA4hKN4hKt3hKF4RZQ4hKtHFLJE2M3gkKtX1Pt3hKtLiK1cEQt3hKYcWdJETSF4hKy3hKt3hKX4BREMjK2PUQ2HGdXAUPt3hSt3hKtX1PtjVTt3hKt3hKtfTZLgGRSUzStETQo4BTDwDU5gka3XUTocVLgYFSS0zQHIzRoE0ZG4BQo4hKL4BUDQ0PD4BR2IzaXgGV1XWPtfmKtjzPtPjPhkjKtXkYPkTbLESUy4BTMEkK14RRm4RTJ4hKHEkb2oTZuQDTt3lPt3hKtnTQtvlKtfzYDokc2g0QQMjKzAkcHMDRmEjTI4hK2fETEsFSrcELtXFVt3hcCg0Z1gkPtXGVo0TLXgGRowDdlYWPv4hKt3BQCMzbDo1TAcmdScTPRwzbPIkQ2cycXQTPt3hKt3hKtX1PBkiK3I0ZXcVQ3wDaE8jKt3hKt3hKtgicXojKtjjZXEzRo8lTI4hKt3hKt3hUAYmPN4haBQzYpgGVl4hKt3hKPEjKtjmKo8lKtjkYmUTXLwFTt3hKt3hKt3BVA4RRj4hcHIEV2gTZAAiRt3hKt3hKt3xPLwlPtvTLXkVSrwDdHkFSDYmcI4BVt3BVLEDUzoldPUTPnwDLyHESoc2PJcGSwbkKt3hKt3hKtLiKlM0QyfGV2vjTLkFNE4hKt3hKt3hKJ4hXvDDcLYzSlQTdXUVPt3hKt3hKtX1PtL0XtPjViYmKGwDaW4hKt3hKt3hK13hKNYDQ4g0cXIzQoQSQt3hKt3hKtXmSt3xZtrRSwXDLxgGVgEjKt3hKt3hKlMjKokjKtj1aSsDVHMDShkTZtfDSB4hKt.ESXgEQSUzYUIkYtHDRlAUdXUUSrsTS2sFVtHlTMQkK18jKy3RPtvDaVYkXCQ0XUUjK1wjQDIzMC4hRI4hKo8FZEYTSVg0MtXWRhMGUBshKlIkPtXGVSk0cPk1cEQkKHIkPt3hcO4hZq4hKLYTTswTLXkVSVgkKt.ETtbyPtHURt3xTigFR33RLXMVPt3hKt3hKq3hcXIjKlc0P3TzS3gTZLgGQ2ETdhIjKtn1PFETREQkYHkVS14xPHYFSrsjK1cGViMVQtDiKt3hKDMjKGEkKtjFMB4hXLY0UWEjYM4hKt3BMt.0TB4hcXQmKtbTZv.SUtf0Pt3hKPoDQPslKtLiTHQES3gkXQUjKt3hKt3BRtLTZE4hKo0TLXkESwfUZA4hRTIlKtXWPPckKtXFSo0DaGkVSwfkKt3hKt3hKh4BSFEjKLECVo0DaLgGRowTPXYVRm4hKtPiYQAEdAIiRBUUajUSRvHlS3rVTiwjQXsTP10jKxQjKzfjcXQjKPYTV1A0So0TLX4BSC4hKt.kStP0Zt3BQ3ckQvbGVo0jQtXmKlcjKDcjKZEkKtfmZAMjQMwlUmEjcL4hKt3BMPcGVBQjKGUVVTcTZAEyTt3xPtLTPP4BQtUTPtfjTFwDQ3gUZqMjK44hKt3hZCITZI4hKJQkYAYDRowDdHkVQyQEZJwFTBYDVPsFUWEjPHYlKBgjYtfGUM41TDk1aqYkKtHkKt3BTH4BQqgjKHUzPk4xcXg0YE4xZD4hKtPjPtXyLt3RVMYjSpwTLXkVPt3hKH4hKu4hcT4hKPQTYXEERo0TLX4hKt3xQt.kRtvDat3xLpMzRpcGVRMFLKwjKt3hKDUjKAkjPtDkKngDYLECVoEjKt3hKt3RTAYGVB4hcXkVSrAUdHkFS3IFTCkVSlcjKHEjQMslZTkTT5MkTAIESlMSQK81L3g0JXMjKogDUA4jZo4xSAEjKkUjTLkFSwvTLt.kRt.kKCYCRmQkQtX1UW4BUMkVSo0jKhQDSGAkYNIkXDEjKHoVQvIFdXkGUC4RahgWPLQkYCkVRP4RZUcGVhwjQt3hK1sDYt4hPFkTPSIDQ1gUULYzQoEjKt3halcjRlYVXVwDatDjd5Y0L1kGS3gTZLcjdt.kKtXGV4YVPQUTVUIESAITUA0jdRsjaQEjXLEyUt3hKt3hKt3hMtXmTEwDZBkkKloTZzTjKt3hKt3hKt3jKXQTPosFTF4ha3gEYA4hKt3hKt3hYC4xSMY1TL4RTDcDSrckKt3hKt3hKtXyMsUkKtPEQtXlKGkVQrUkKt3hKt3hcN4hKv3BLtcmPZI1cX4hKt3hKt3hKtX1PtjVPPEkTA4hKNgzPMYGRCQjQLIjKt3hcN4BRUUUSIQzTEEjPHYFQ4gETy3BQ3gDdX4hXB4hKt3BRt.EQH4hX1MTTPgGVU81PtzlKt3hKtHjKoETPtXjd1IDVXMUUoEjcI4hKt3xLtXmUD4hKF8DQ2kTZUUDRtHlPt3hKt3jKLYTPtXlKC8DUA0TUMYjKs4hKt3hYD4hU24hKmA0YF0FSVUELtXWRt3hKtfTP1gkQtXGVo0TLXgGRowDdT4xPLYGTA4hYBMzPEoGUCUDQQUTPnwzcLECVo0TLXkVSF4xPMYjKt3hLtj1XtPTZMECVo0TLXkVP1AUZMYjKtvDTW4hK3gUZMYTTo0TLX4hb3gUZA4hPCwTLAwDSwfUZMECVo0jQtDGSwfkKlcmKoEkKHkVSwfUZMECVoEjKE4BSF4BTLYGVGYlcTkVSwfUZMECVt.UPtjVPt3xPtUzPM0TLXkVSrwDdHkFSkolKt3hKt3RdlcGTxAEQKUTRFsjQAIDRXY1ZKslc4gkKt3hKt3hKtLCS1gkTh4xQXEzTIcCSF4hKt3hKt3hKNMDSrMTRtHjUzQkPOkVPt3hKt3hKtXVdtj1a1MjZps1RqYWdX4hKt3hKt3hKyvjcXojKPsDVzHUR2vjQt3hKt3hKt3hSCwjQAsDSFYUcXgGVoEjKt3hKt3hKlkmKoEkKtjVSwfUZIkFS3gTdGgDSF4hKtXWSLAUUiQWTwPkdEYzXoQyZHQFRQkTZiQjQtfkPtDzc1QDTpklQHI1YGo0L3gUTUMjK3gEQt7DRVIjbP4hKjgEdLMGSFIkXtXmR3.0ctnEQQ4jPt.0RWAEdJk1bT0jKt3hKt3hcLYDSr4hKLEiQ23VTRkVPt3hK2DkPCYVTCkVRt3RZUEURvwTLXEVPt3hKt3hKpslcXIjK1gUZMECV3gTZLgGV1MDVpMkPYQzPCMmXvLkPIQzTEEjTLMmZCgTSzbGVo81PtnjKt3BQlMjPoEjKtrzLQYjXLECVt3hYB4hKtDzLl4xUJ4hYFcTT2kTZMYjKt3hKt3BTt3DR5UTPt3lcXQkZ3gUZA4hKt3hKt3hYCEzXAAkKRwjQEkVSwfkKt3hKt3hKtLiYlYEQt3xQoE0cHkVSVQjKt3hKt3hKNQDSF4hKLwFVKcWZLgGRowDTLYGRYEjKtfjYmEUR2QTUEkTUKM0XEQEUt4xQXMCLT4RPloTLt.kKyXmKPYjK1cDRhEzQoM1ZP4hcREjSL4hSHY2Zt3haDwDSPIEUoEEQtTmYPMjKlMTQokjKtfkaRMjRLYzUBEDTKkjct3xLt.0SD4hYGQmYtLTZMECTtnmPBwDQt3jKPslKtXmZDQjcBUUZYQjKx4FTC4hKGUTZI4hKj0jdWcCRowDdHklKNY1PQ4xM4UDVLUETHUjZTETPBgjYtfGVoEUTNkVSrIjKt3hKt3hKN4hbogTZiYGVos1cXkVSF4hKt3hKtX1PtLGVQ0TZLECViwTLXkVPt3hKt3hKy3hcXoja3UTZMYkQo0TLX4hKt3hKt3hStvDaCczbmUTZuIUUo0jQt3hKt3hKlMjKRkjPt3FSwfkZLECVoEjKt3hKt3BTAYGVTgETPkVSwfEdHkFS3MiYAklKt3hKDMjKEcGUQMTTqQ0SzPDR2wjQt3hK1gUZMYjKO4hKtPjXt3BSI4hKK8FdQgFSwfUZAY2Pt3hKAkWP1gkPtXGVHgSTD4BVD4hK23hKt.kcO4BSFQjKLECVpwDdXkVPt3xSt3hKDI2PtjVRt3RZA4hKtvTLXkVP1MjKt3RPsEDTU4hKtzDbhoFRo0TLX4xMt3hKPYGVtvDat3BSwfUZMwFS3gTZLc0M1YjatDjKlY1YPEDM5I0T2IDRTQiPHgESwfUV5cmQkwjQt3hKt3hcA4hUt3hcXkVSrYjQUMTSoEjKt3hKtHjKXQkKtnmcXk1XQMUS3PjKt3hKt3hYC4RS24hK0vTLXsFSwfUZA4hKt3hKtLiK1gkPtXGVo0TLE0DL5MUZA4hKt3hKN4BUDMDVpcGVoUEdXkVSF4hKt3hKtXVPtXUTtXTZMECVokTZLgGRCIjSpYmKG4hKDwDSEEVciICSDEjPTcVTV4jY5o1Qo0DaN4hat3hKP4BSDwjUtjkblcTV1cGVoEjKtnjKt3BQlMTPhclKtnkXDUTaLECVt3hKt3hKtDDRQA0U4QkKBoDTQoTZMYjKt3hKt3hKt3TQ5s1PtfzcXQET3gUZA4hKt3hKt3hKTEjVQ4hKhwjQEkFSwfUTt3hKt3hKtLCU1gEStXFVnMGQOgGRowDdtbmKowDaBgjKCMDSYo2TlwDLUUTUDQkYlACNh.hXgMWY1PiNvI2amIWXs0iHwXSLtbFMlYUT3fVUzomKt3hKt3hKt3hKtPjPt7DQ2ITTYolSNgSdSoEQE4hKt3hKt3hKt3xMD4xQ1clKkgyYtLDMm4DUqUjKt3hKt3hKt3hKXMjKY4VZBgURqMTQq4BSYkUPt3hKt3hKt3hKtXGQtXDSvHTRQIkSGAEdtnmcA4hKt3hKt3hKt3hZt3RVLcWPKQDaWslKnMTZ1IjKt3hKt3hKt3hKyHjKioFUAwlX2MUVLAkUgMGLGEjKtvTQYYlRAAkKtfESUgEMAIETsUjUZQGM38jKt3hKt3hKh7hO7zVZjk1PC8hO77BYkgWYjMEcgQWY9.fVSEVdfDzYgklat..B.jA.l.vJ.fC..A.R.zD.eA.Y.jVAQU.UEXUAYUvVEHVAmUPZE3VGy........HP..........TA..................zgO"
						}
,
						"snapshotlist" : 						{
							"current_snapshot" : 0,
							"entries" : [ 								{
									"filetype" : "C74Snapshot",
									"version" : 2,
									"minorversion" : 0,
									"name" : "Dexed",
									"origin" : "Dexed.component",
									"type" : "AudioUnit",
									"subtype" : "Instrument",
									"embed" : 1,
									"snapshot" : 									{
										"pluginname" : "Dexed.component",
										"plugindisplayname" : "Dexed",
										"pluginsavedname" : "/Library/Audio/Plug-Ins/Components/Dexed.component",
										"pluginsaveduniqueid" : 0,
										"version" : 1,
										"isbank" : 0,
										"isbase64" : 1,
										"blob" : "7560.hAGaoMGcv.C1AHv.DTfAGfPBJr.DQHwDTvUag4VclE1XzUmbkIGUjEFcgwUYrUVak4Fcs3VXsU1UyUmXzkGbkckckI2bo8laTQWdvU1WP7fZ0MVYPwVcmklaSQWXzUFUtEVakIAQGMkPOEAAjC..............aB....yO.B......w.........fL+.H......LyO........z7Cf......PM+.H......XyO.B......23SsBXI....N.........jC.......fAe........X.H+.H.....FDB.......fAh7C......XvH9rca2B..FPxO.B....fAk7Cf.....XfI+.H.....FbxO.B....fAn7S.J0O..XfO+DfR8C..F7yOAnT+..fA.8S.J0O..XPP+Ti.VB..FHjON6sX..fAC4S+pU...X.Q+.H.....FTzO.B....fAF8SalSB..XvQ........FzE.......fAd8Cf.....XvW........F.VODDBB..fAgA.......XfX+.......FLF.......fAjA.......XPY........FXF.......fA7A.......XPe........F3G.......fA+A.......X.f+.H.....FDnOApT+..fAB9SI9UK..Xvf9zuZE...FP3O.B....fAE9S.J0O..Xvl+.H.....FvI.......fAcB.......Xfm+.H.....F7I.......fAfB.......XPn........FH5O......fAiB.......X.o........FnK.......fA6B.......X.u........FzK.......fA9B.......Xvu........F.7O.B....fAA6yFlnL..Xfv+The0B..FLrO8qVA..fAY+Cf.....Xf19Lti4...Fr8O.B....fAbC.......XP2........F38O.B....fAeC.......X.38PXHH...FDN.......fAh+C......X.9........FjO.......fA5C.......Xv9........FvO.......fA8C.......Xf+........F7O.......vA.7Cf.....bP.9XfcyC..GbwOk3Ws..vAX3S+pU...bPF+.H.....GngOsaNI..vAa7Cf.....b.G........GzA.......vAd7Cf.....bvG........G.B.......PuwC.......zq7+.......8NO.......PuzC.......za8........8ZO.......Pu2C.......zK9........8lO.......Pu5C.......3KD+.H.....9FQON6sX..fuR7SI9UK..36D9zuZE...9RwO.B....fuU3S6lSB..3qE+.H.....9dA.......fuX........3aF+.H.....99B.......fuvzCggf...3aL........9JyO......fuy........3KM........9VC.......fu1........36M........9hC.......fuNA.......36S........9B0O.B....fuQ0CjN6M..3qT+The0B..9NkOnq6K..fuT8Cf.....3aU9fttu...9Z0O.B....fuWA.......3aa........951O.B....fuuA.......3Kb........9FG.......fux8C......36b........9RG.......fu0A.......3qc........9xH.......fuMB.......3qi........99H.......fuP9Cf..PzLzPTxDsCODELV8TczAWczIAQkgGYP.fDgUWa08TDWDrUCISH3dA..vyO30FafXWYxMWZu4VOhDiKvHBHk41XuQVZtcVOhTEUF0BNh7iOfvCYkgWYjMEcgQWYfLVcz8lYl0iHw3BLh.hbkM2a8HBLt.iHfbVXo4VOhDiKvHBHiUmbxUlazAkbuclbg0VOh.iHfz1at8VSuQVY8HBLh.RYtcVZtUFU4AWY8HRLh.RagMGckIGU04VY8HBLh.xavM0coQ2Xn0iHwDSLwDSLh.BcxElayA2ayUVLxDzbSMVXrUVOhDiHfzFbkUjagIFakQVOh.iHfzFbkAUZzMFZBUlajIUXtcVY8HhLzHBH2gVYkwVSuQVOh.CHv.BLf.iHfX1auQWSuQVOh.CHv.BLf.iHfHlbkEFcn0zaj0iHv.BLf.CHvHBHgYFckIGcuU2Xn0zaj0iHv.BLf.CHvHhO7PVY3UFYBw1ahAhXgMWY1PiNyk2bkgWOhPSLvPiK18DQtjjKB4xQtP0RoACdX4hKt3hKt3hKy3hcX4hKlIjKEkGVzwjQt3hKt3hKt3hStvjQA4hdt.0cLw1RoEjKt3hKt3hKlMjKoEjKt7jKTwTZ2gGVt3hKt3hKt3xLtXGVD4BTF4RQ4gEdLYjKt3hKt3hKt3jKLYjKtfEQJcGSwfkXA4hKt3hKt3hYC4RZI4hKo0TLXkVRowDdHk2QOwjPt3hKPwDVLUEVzDjTP0VQVoEczHjTL8lKHkVUEQkKDMjKt3hKNgDTEUjK1QkTJY2cXI1aE4Bdt3hKtXVPAoUTt3xctolPlgDaXgVPPoDNtnlPHclcQQjK10zStY2RocWQW4hY4YkKL4hXDwjQA4hXCgjY5E0Uj8VQtPTP1gkPt3RPXEETtHiYoITcLwFVtDjcIkVP1MDVmYFVDQjYXgVRrgELDkFS3MicCcFSBQjKtDzPLUDUUI0ZTEkYtHDRlwDaKECUvfkYMYjKz3hKt3haCETZUYmToQCZHEVSwbUZA4hKt3hKtjWPlM0QDMjUIU0TWkFLD4hKt3hKt3hYhIlbEQzPlUjS2nGLX0TPt3hKt3hKtvTQE8TRtbDVmMzSi0jUS4hKt3hKt3hKoY1cTIDRrMkY1IzSoUUQt3hKt3hKtXlRtvjQtbDVUcUZMYjK54BTWE0M1gjKt3hK24hYPsVQFM1bUYjV3EEahkVVRYzaLYjTHEjcI4BQ1MjcQYFUD4hcX0lZQgTZiQDTtHlPt3xMtHlKPMTPtvjQSkFN3gEVAYjKs4hKt7jKG4hXI4hKoMlTFcFSwDkKAYWRtPjcCMCT1gEQtXGVroVPIk1YDIkKhIjKtbiKN4xLDIjKLYzTogCdXgUPF4Rat3hKOY1Pt3BRt3BU3.yU2fTZLgGR4cjSTIjKt3hKPgkKEIUPIAyTHEjPHYlK3gkcD4hQjgCQt3hco0jKDYWTLwDaG4xMvfDR1cGVFEjKtnmK1gzP1UDQOkkKtTVPRYzYLwVTt3hKt3hKt3RXhcGVB4BTUgGRlITZYQjKt31PtrlK1IjK2nFQtHmZKAkc1gkQA4hK5YlKtLjbBMzSQ4hKJQycFUFSrEkKt3xSt3hKtj1X2gkPtX1UCgSQOgGRowDdHY1PnQjPt3hZAMzPmwlX0AiUXYFUCgjXUs1SXoGdXkVPt3hYt3hKCA0ctvzaPQEUukFQpwjUW4hKtfjKHEjK1XWTVQjK1U0bxE0Ro0jQt3hK3gkKLYlKPwDat3BUq8DVyfGVoEjKtXlKt3xP14hKG8FTtX0aoQjZLY0Ut3hKH4BRA4xPPEkUDQjKVMmbQsTZMYjKt3BdX4BSl4BTLwlKA4hKt3hKlwDdHkFSCYFTF4hat3BR14xTmk0UZoWQrIlYtHzUt3hKDUFSwfUZA4hKt.kKt.UStPkPtXVTt3RTEEVSwfkKt3hKt3hKT4xLp4hKyHjKOgkPWkVSF4hKt3hKt3RQtjVRt3hKt3hKlwTLXkVPt3hKt3hKtgjKT4BSrwjKpYFQl0TLX4hYA4RQt3hStfTQtjFMB4hXXI0Uo0jQt3hKt3hKt3hKoUDTAkVSwfUZIkFS3gTdtrjXA4xSt.EQLwTQgUWSvLlbAg2R0Y2ZSUVV5ITZAEiTtH1PtDlKPIlK2LTPtXFZGkET3gkVuUjK44hKt3BQ24RZI4hK4byZQwDSFg0SA4BStLSPtjkKtDEQt3hRjoVPIk1aqYkKLMjKt3BTXcESr4RPpk2UFMmcXY1bE4BZtXFRtnlQtfTRt3hayDkQpwDaVoUP1wjKt3hKIwzcXIjKP4zTAUTUwwTZLgGUPEjXtjFRoclPF8TRDgzQUwVXwrFaiIVSwTzRyXGVYcWQt7jKt3BQXUjKv.0TtHDM1IjXyTkUZEjcC4hKtDjUQ4hTF4hKV4DSpkTZqASTtbiKt3BTlsjKls1RtX1ZCczX3gUVmUjKO4hKtPzLC4xYI4hKnETLFAGSFcjTAY2PtLiKAYWPtfEQ2HCVJIlKKkVPVYkK23hKNAkKh4BSF4hKLECVo0TLIgGUosjS2.UPtvjQtnWP1QUPiUDREACQHUUPEgTdtgGRQwTLXkVPlcjKX4hKl0jKKIjK1wTTHgVQo0TLX4xLA4RTt3BVBwDat3hankDUybGVo0jQtXlKt3hKtXjPokjKt.iaRkTVLECVo0DaG4BSt3hKMY1StvjUMEER3UTZMECVtLSPtzjKt.kPHYjKo8FZIQ0M2gUZMYjKl4hKt3hKDITZAYGVo0TLTkFN30DdHkmKMQjKt3BUEIDS1oVTOkTUYUSP3oTb1ACVXwjQJ4hK1gkKt3hKt3BTN4hKl4hKLYDRoclPt3BSF4hKt3hKtn1PtjVP1wTZMgGVt4hKtfVPt3hKt3hKz3hcX4hK1gUaLYjRt3hcX4hKt3hKt.kStvDat3BSVsTZmIjKtvjQt3hKt3hKpMjKokjYFkVS3gkaLESTt3hKt3hKt3BMtXGVBomcXkVSFoDdHkFS3cSPBQ0MpcjPhEjQEQidP8TUqMEUUoFUSMmcCckYoM0RMYjKt3hKt3hKG4RZUAURo0TLXICSwfUZA4hKt3hKtXWPlckKtXmPOIVTN4zb5gkKt3hKt3hKF4BSVEDaLECVocVdXkVSF4hKt3hKt3hKtPVPt3xR2XWQwLidRkVPt3hKt3hK1EjcXUDV3gUZMYUSo0TLX4hKt3hKt3hStLSQt3BSFcTZMwFS3gTZLQzMlsjKy.0RvXVPU4VUsElZUwlXl4BdL4BUUMTbHkGVt3hYC4hKt3hSAYGUH4hKCcUU3oDLLYjKtLiKt3hKtPjKLYTPtn1cUglbn4TZA4hKN4hKt3hKF4RZQ4hKtHFLJE2M3gkKtX1Pt3hKtLiK1cEQt3hKYcWdJETSF4hKy3hKt3hKX4BREMjK2PUQ2HGdXAUPt3hSt3hKtX1PtjVTt3hKt3hKtfTZLgGRSUzStETQo4BTDwDU5gka3XUTocVLgYFSS0zQHIzRoE0ZG4BQo4hKL4BUDQ0PD4BR2IzaXgGV1XWPtfmKtjzPtPjPhkjKtXkYPkTbLESUy4BTMEkK14RRm4RTJ4hKHEkb2oTZuQDTt3lPt3hKtnTQtvlKtfzYDokc2g0QQMjKzAkcHMDRmEjTI4hK2fETEsFSrcELtXFVt3hcCg0Z1gkPtXGVo0TLXgGRowDdlYWPv4hKt3BQCMzbDo1TAcmdScTPRwzbPIkQ2cycXQTPt3hKt3hKtX1PBkiK3I0ZXcVQ3wDaE8jKt3hKt3hKtgicXojKtjjZXEzRo8lTI4hKt3hKt3hUAYmPN4haBQzYpgGVl4hKt3hKPEjKtjmKo8lKtjkYmUTXLwFTt3hKt3hKt3BVA4RRj4hcHIEV2gTZAAiRt3hKt3hKt3xPLwlPtvTLXkVSrwDdHkFSDYmcI4BVt3BVLEDUzoldPUTPnwDLyHESoc2PJcGSwbkKt3hKt3hKtLiKlM0QyfGV2vjTLkFNE4hKt3hKt3hKJ4hXvDDcLYzSlQTdXUVPt3hKt3hKtX1PtL0XtPjViYmKGwDaW4hKt3hKt3hK13hKNYDQ4g0cXIzQoQSQt3hKt3hKtXmSt3xZtrRSwXDLxgGVgEjKt3hKt3hKlMjKokjKtj1aSsDVHMDShkTZtfDSB4hKt.ESXgEQSUzYUIkYtHDRlAUdXUUSrsTS2sFVtHlTMQkK18jKy3RPtvDaVYkXCQ0XUUjK1wjQDIzMC4hRI4hKo8FZEYTSVg0MtXWRhMGUBshKlIkPtXGVSk0cPk1cEQkKHIkPt3hcO4hZq4hKLYTTswTLXkVSVgkKt.ETtbyPtHURt3xTigFR33RLXMVPt3hKt3hKq3hcXIjKlc0P3TzS3gTZLgGQ2ETdhIjKtn1PFETREQkYHkVS14xPHYFSrsjK1cGViMVQtDiKt3hKDMjKGEkKtjFMB4hXLY0UWEjYM4hKt3BMt.0TB4hcXQmKtbTZv.SUtf0Pt3hKPoDQPslKtLiTHQES3gkXQUjKt3hKt3BRtLTZE4hKo0TLXkESwfUZA4hRTIlKtXWPPckKtXFSo0DaGkVSwfkKt3hKt3hKh4BSFEjKLECVo0DaLgGRowTPXYVRm4hKtPiYQAEdAIiRBUUajUSRvHlS3rVTiwjQXsTP10jKxQjKzfjcXQjKPYTV1A0So0TLX4BSC4hKt.kStP0Zt3BQ3ckQvbGVo0jQtXmKlcjKDcjKZEkKtfmZAMjQMwlUmEjcL4hKt3BMPcGVBQjKGUVVTcTZAEyTt3xPtLTPP4BQtUTPtfjTFwDQ3gUZqMjK44hKt3hZCITZI4hKJQkYAYDRowDdHkVQyQEZJwFTBYDVPsFUWEjPHYlKBgjYtfGUM41TDk1aqYkKtHkKt3BTH4BQqgjKHUzPk4xcXg0YE4xZD4hKtPjPtXyLt3RVMYjSpwTLXkVPt3hKH4hKu4hcT4hKPQTYXEERo0TLX4hKt3xQt.kRtvDat3xLpMzRpcGVRMFLKwjKt3hKDUjKAkjPtDkKngDYLECVoEjKt3hKt3RTAYGVB4hcXkVSrAUdHkFS3IFTCkVSlcjKHEjQMslZTkTT5MkTAIESlMSQK81L3g0JXMjKogDUA4jZo4xSAEjKkUjTLkFSwvTLt.kRt.kKCYCRmQkQtX1UW4BUMkVSo0jKhQDSGAkYNIkXDEjKHoVQvIFdXkGUC4RahgWPLQkYCkVRP4RZUcGVhwjQt3hK1sDYt4hPFkTPSIDQ1gUULYzQoEjKt3halcjRlYVXVwDatDjd5Y0L1kGS3gTZLcjdt.kKtXGV4YVPQUTVUIESAITUA0jdRsjaQEjXLEyUt3hKt3hKt3hMtXmTEwDZBkkKloTZzTjKt3hKt3hKt3jKXQTPosFTF4ha3gEYA4hKt3hKt3hYC4xSMY1TL4RTDcDSrckKt3hKt3hKtXyMsUkKtPEQtXlKGkVQrUkKt3hKt3hcN4hKv3BLtcmPZI1cX4hKt3hKt3hKtX1PtjVPPEkTA4hKNgzPMYGRCQjQLIjKt3hcN4BRUUUSIQzTEEjPHYFQ4gETy3BQ3gDdX4hXB4hKt3BRt.EQH4hX1MTTPgGVU81PtzlKt3hKtHjKoETPtXjd1IDVXMUUoEjcI4hKt3xLtXmUD4hKF8DQ2kTZUUDRtHlPt3hKt3jKLYTPtXlKC8DUA0TUMYjKs4hKt3hYD4hU24hKmA0YF0FSVUELtXWRt3hKtfTP1gkQtXGVo0TLXgGRowDdT4xPLYGTA4hYBMzPEoGUCUDQQUTPnwzcLECVo0TLXkVSF4xPMYjKt3hLtj1XtPTZMECVo0TLXkVP1AUZMYjKtvDTW4hK3gUZMYTTo0TLX4hb3gUZA4hPCwTLAwDSwfUZMECVo0jQtDGSwfkKlcmKoEkKHkVSwfUZMECVoEjKE4BSF4BTLYGVGYlcTkVSwfUZMECVt.UPtjVPt3xPtUzPM0TLXkVSrwDdHkFSkolKt3hKt3RdlcGTxAEQKUTRFsjQAIDRXY1ZKslc4gkKt3hKt3hKtLCS1gkTh4xQXEzTIcCSF4hKt3hKt3hKNMDSrMTRtHjUzQkPOkVPt3hKt3hKtXVdtj1a1MjZps1RqYWdX4hKt3hKt3hKyvjcXojKPsDVzHUR2vjQt3hKt3hKt3hSCwjQAsDSFYUcXgGVoEjKt3hKt3hKlkmKoEkKtjVSwfUZIkFS3gTdGgDSF4hKtXWSLAUUiQWTwPkdEYzXoQyZHQFRQkTZiQjQtfkPtDzc1QDTpklQHI1YGo0L3gUTUMjK3gEQt7DRVIjbP4hKjgEdLMGSFIkXtXmR3.0ctnEQQ4jPt.0RWAEdJk1bT0jKt3hKt3hcLYDSr4hKLEiQ23VTRkVPt3hK2DkPCYVTCkVRt3RZUEURvwTLXEVPt3hKt3hKpslcXIjK1gUZMECV3gTZLgGV1MDVpMkPYQzPCMmXvLkPIQzTEEjTLMmZCgTSzbGVo81PtnjKt3BQlMjPoEjKtrzLQYjXLECVt3hYB4hKtDzLl4xUJ4hYFcTT2kTZMYjKt3hKt3BTt3DR5UTPt3lcXQkZ3gUZA4hKt3hKt3hYCEzXAAkKRwjQEkVSwfkKt3hKt3hKtLiYlYEQt3xQoE0cHkVSVQjKt3hKt3hKNQDSF4hKLwFVKcWZLgGRowDTLYGRYEjKtfjYmEUR2QTUEkTUKM0XEQEUt4xQXMCLT4RPloTLt.kKyXmKPYjK1cDRhEzQoM1ZP4hcREjSL4hSHY2Zt3haDwDSPIEUoEEQtTmYPMjKlMTQokjKtfkaRMjRLYzUBEDTKkjct3xLt.0SD4hYGQmYtLTZMECTtnmPBwDQt3jKPslKtXmZDQjcBUUZYQjKx4FTC4hKGUTZI4hKj0jdWcCRowDdHklKNY1PQ4xM4UDVLUETHUjZTETPBgjYtfGVoEUTNkVSrIjKt3hKt3hKN4hbogTZiYGVos1cXkVSF4hKt3hKtX1PtLGVQ0TZLECViwTLXkVPt3hKt3hKy3hcXoja3UTZMYkQo0TLX4hKt3hKt3hStvDaCczbmUTZuIUUo0jQt3hKt3hKlMjKRkjPt3FSwfkZLECVoEjKt3hKt3BTAYGVTgETPkVSwfEdHkFS3MiYAklKt3hKDMjKEcGUQMTTqQ0SzPDR2wjQt3hK1gUZMYjKO4hKtPjXt3BSI4hKK8FdQgFSwfUZAY2Pt3hKAkWP1gkPtXGVHgSTD4BVD4hK23hKt.kcO4BSFQjKLECVpwDdXkVPt3xSt3hKDI2PtjVRt3RZA4hKtvTLXkVP1MjKt3RPsEDTU4hKtzDbhoFRo0TLX4xMt3hKPYGVtvDat3BSwfUZMwFS3gTZLc0M1YjatDjKlY1YPEDM5I0T2IDRTQiPHgESwfUV5cmQkwjQt3hKt3hcA4hUt3hcXkVSrYjQUMTSoEjKt3hKtHjKXQkKtnmcXk1XQMUS3PjKt3hKt3hYC4RS24hK0vTLXsFSwfUZA4hKt3hKtLiK1gkPtXGVo0TLE0DL5MUZA4hKt3hKN4BUDMDVpcGVoUEdXkVSF4hKt3hKtXVPtXUTtXTZMECVokTZLgGRCIjSpYmKG4hKDwDSEEVciICSDEjPTcVTV4jY5o1Qo0DaN4hat3hKP4BSDwjUtjkblcTV1cGVoEjKtnjKt3BQlMTPhclKtnkXDUTaLECVt3hKt3hKtDDRQA0U4QkKBoDTQoTZMYjKt3hKt3hKt3TQ5s1PtfzcXQET3gUZA4hKt3hKt3hKTEjVQ4hKhwjQEkFSwfUTt3hKt3hKtLCU1gEStXFVnMGQOgGRowDdtbmKowDaBgjKCMDSYo2TlwDLUUTUDQkYlACNh.hXgMWY1PiNvI2amIWXs0iHwXSLtbFMlYUT3fVUzomKt3hKt3hKt3hKtPjPt7DQ2ITTYolSNgSdSoEQE4hKt3hKt3hKt3xMD4xQ1clKkgyYtLDMm4DUqUjKt3hKt3hKt3hKXMjKY4VZBgURqMTQq4BSYkUPt3hKt3hKt3hKtXGQtXDSvHTRQIkSGAEdtnmcA4hKt3hKt3hKt3hZt3RVLcWPKQDaWslKnMTZ1IjKt3hKt3hKt3hKyHjKioFUAwlX2MUVLAkUgMGLGEjKtvTQYYlRAAkKtfESUgEMAIETsUjUZQGM38jKt3hKt3hKh7hO7zVZjk1PC8hO77BYkgWYjMEcgQWY9.fVSEVdfDzYgklat..B.jA.l.vJ.fC..A.R.zD.eA.Y.jVAQU.UEXUAYUvVEHVAmUPZE3VGy........HP..........TA..................zgO"
									}
,
									"fileref" : 									{
										"name" : "Dexed",
										"filename" : "Dexed_20231218.maxsnap",
										"filepath" : "~/Documents/Max 8/Snapshots",
										"filepos" : -1,
										"snapshotfileid" : "3a6d1b5d9ee5228cd0ab61aa0e3084ea"
									}

								}
 ]
						}

					}
,
					"text" : "audiounit~",
					"varname" : "vst~",
					"viewvisibility" : 0
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-107", 1 ],
					"midpoints" : [ 241.0, 188.0, 82.5, 188.0 ],
					"source" : [ "obj-1", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-107", 0 ],
					"midpoints" : [ 215.428571428571445, 190.0, 31.5, 190.0 ],
					"source" : [ "obj-1", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-42", 0 ],
					"source" : [ "obj-1", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-21", 2 ],
					"source" : [ "obj-103", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-21", 1 ],
					"source" : [ "obj-105", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-108", 0 ],
					"source" : [ "obj-107", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-109", 0 ],
					"source" : [ "obj-108", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-1", 0 ],
					"midpoints" : [ 458.10714285714289, 129.0, 215.428571428571445, 129.0 ],
					"source" : [ "obj-11", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-41", 0 ],
					"source" : [ "obj-11", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"midpoints" : [ 496.10714285714289, 278.0, 266.571428571428612, 278.0 ],
					"order" : 1,
					"source" : [ "obj-11", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-86", 0 ],
					"midpoints" : [ 496.10714285714289, 276.0, 210.0, 276.0, 210.0, 463.0, 313.571428571428612, 463.0 ],
					"order" : 0,
					"source" : [ "obj-11", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-86", 0 ],
					"midpoints" : [ 170.5, 460.0, 313.571428571428612, 460.0 ],
					"source" : [ "obj-120", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"midpoints" : [ 211.428571428571445, 276.0, 266.571428571428612, 276.0 ],
					"source" : [ "obj-136", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"midpoints" : [ 155.5, 276.0, 266.571428571428612, 276.0 ],
					"source" : [ "obj-138", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-11", 0 ],
					"source" : [ "obj-15", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-1", 0 ],
					"midpoints" : [ 542.0, 177.0, 399.0, 177.0, 399.0, 144.0, 215.428571428571445, 144.0 ],
					"source" : [ "obj-21", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"color" : [ 0.986251831054688, 0.007236152887344, 0.027423052117229, 1.0 ],
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-21", 3 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"midpoints" : [ 580.0, 270.0, 266.571428571428612, 270.0 ],
					"source" : [ "obj-21", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-99", 0 ],
					"midpoints" : [ 618.0, 270.0, 507.0, 270.0, 507.0, 387.0, 313.571428571428612, 387.0 ],
					"source" : [ "obj-21", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-21", 0 ],
					"source" : [ "obj-26", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-1", 0 ],
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-60", 3 ],
					"midpoints" : [ 693.5, 345.0, 369.0, 345.0, 369.0, 345.0, 353.571428571428612, 345.0 ],
					"source" : [ "obj-39", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-42", 0 ],
					"midpoints" : [ 420.10714285714289, 191.0, 266.571428571428612, 191.0 ],
					"source" : [ "obj-41", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-43", 0 ],
					"source" : [ "obj-42", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"source" : [ "obj-43", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-60", 2 ],
					"midpoints" : [ 521.571428571428669, 337.5, 324.571428571428612, 337.5 ],
					"source" : [ "obj-5", 3 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-60", 1 ],
					"midpoints" : [ 351.571428571428612, 325.0, 295.571428571428612, 325.0 ],
					"source" : [ "obj-5", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-60", 0 ],
					"source" : [ "obj-5", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-86", 0 ],
					"midpoints" : [ 125.928571428571445, 456.0, 313.571428571428612, 456.0 ],
					"source" : [ "obj-57", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"midpoints" : [ 113.5, 271.75, 266.571428571428612, 271.75 ],
					"source" : [ "obj-58", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"color" : [ 0.131302371621132, 0.99969744682312, 0.023593800142407, 1.0 ],
					"destination" : [ "obj-1", 0 ],
					"midpoints" : [ 266.571428571428612, 386.0, 192.0, 386.0, 192.0, 138.0, 215.428571428571445, 138.0 ],
					"source" : [ "obj-60", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-99", 1 ],
					"source" : [ "obj-60", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-86", 0 ],
					"midpoints" : [ 225.428571428571445, 456.0, 313.571428571428612, 456.0 ],
					"source" : [ "obj-7", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"midpoints" : [ 68.5, 276.0, 266.571428571428612, 276.0 ],
					"source" : [ "obj-9", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"color" : [ 0.986251831054688, 0.007236152887344, 0.027423052117229, 1.0 ],
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-99", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-86", 0 ],
					"source" : [ "obj-99", 0 ]
				}

			}
 ],
		"parameters" : 		{
			"obj-1" : [ "vst~", "vst~", 0 ],
			"parameterbanks" : 			{
				"0" : 				{
					"index" : 0,
					"name" : "",
					"parameters" : [ "-", "-", "-", "-", "-", "-", "-", "-" ]
				}

			}
,
			"inherited_shortname" : 1
		}
,
		"dependency_cache" : [ 			{
				"name" : "Dexed_20231218.maxsnap",
				"bootpath" : "~/Documents/Max 8/Snapshots",
				"patcherrelativepath" : "../../Documents/Max 8/Snapshots",
				"type" : "mx@s",
				"implicit" : 1
			}
, 			{
				"name" : "param_scaler.js",
				"bootpath" : "~/Desktop/preset_renderer",
				"patcherrelativepath" : ".",
				"type" : "TEXT",
				"implicit" : 1
			}
 ],
		"autosave" : 0,
		"bgcolor" : [ 0.32549, 0.345098, 0.372549, 1.0 ],
		"editing_bgcolor" : [ 0.65098, 0.666667, 0.662745, 1.0 ]
	}

}

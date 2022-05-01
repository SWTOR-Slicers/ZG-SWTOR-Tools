# ZeroGravitas' SWTOR Tools.

This Blender Add-on provides with a miscellanea of tools to use on **Star Wars: The Old Republic**'s game assets, including an Uber Materials Processor for static game models. It will grow in features as they occur to me 😛. Quality of code-wise, "this is not a place of honor". Still, it works, kindasorta.

* [Installation.](#installation)
* [Materials Tools:](#swtor-materials-tools)
  * [Process Uber Materials.](#process-uber-materials)
  * [Deduplicate Scene's Nodegroups.](#deduplicate-scenes-nodegroups)
  * [Set Backface Culling On/Off.](#set-backface-culling-onoff)
* [Objects Tools:](#swtor-objects-tools)
  * [Quickscaler.](#quickscaler)
  * [Merge Double Vertices.](#merge-double-vertices)
  * [Modifiers Tools.](#modifiers-tools)
* [Misc. Tools:](#swtor-misc-tools)
  * [Simplify Scene.](#simplify)
  * [Switch Skeleton between Pose and Rest Position.](#pose-position--rest-position)


## Installation.

The installation of the Add-on in Blender follows the usual directions:

1. [**Download the Add-on's "zg_swtors_tool.zip" file from this link**](https://github.com/ZeroGravitasIndeed/zg_swtor_tools/raw/main/zg_swtor_tools.zip). Don't unZip it: it's used as such .zip.
2. In Blender, go to Edit menu > Preferences option > Add-ons tab > Install… button.
3. Select the Add-on in the file dialog box and click on the Install Add-on button.
4. The Add-on will appear in the Add-ons list with its checkbox un-ticked. Tick it to enable the Add-on.
5. Twirl the arrow preceding the check-box to reveal some information and, most importantly, **the Add-on's Preferences**. Note that it asks for **the path of a "resources" folder**.

      ![](https://github.com/ZeroGravitasIndeed/zg_swtor_tools/blob/main/documentation/010.png)

    Some of the Add-on's features depend on looking for information and game assets inside a SWTOR assets extraction (typically produced by apps such as SWTOR Slicers or EasyMYP). In the case of a SWTOR Slicers extraction, the "resources" folder is inside the folder set as that app's Output Folder.
    
    Click on the folder icon to produce a file browser dialog window where to locate the "resources" folder, or type or copy the folder path inside the filepath field.
        
The Add-on's tools will appear in the 3D Viewport's Sidebar ('n' key), in the "ZG SWTOR" tab.

![](https://github.com/ZeroGravitasIndeed/zg_swtor_tools/blob/main/documentation/020.png)

The current tools are:

## SWTOR Materials Tools:

### Process Uber Materials.
Processes all the Uber-type materials detected in a selection of objects, locating their related texturemaps and linking them to a SWTOR Uber shader (modern or legacy, whichever are active). It processes any EmissiveOnly-type (glass) materials, too. It's particularly fast, as it (only) works with an asset extraction's "resources" folder.

Options:
* **Overwrite Uber Materials** (off by default): overwrites already present Uber and EmissiveOnly objects's materials, which allows for regenerating materials that might have lost texturemaps, converting Uber materials from Legacy to modern and viceversa, etc. The option appears in the Undo box at the bottom-left side of the 3D Viewport.
* **Collect Collider Objects** (on by default): adds all objects with an "Util_collision_hidden" material to a Collection named "Collider Objects".

**It needs the presence of an enabled [SWTOR importer Add-on ("io_scene_gr2")](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x)** in Blender, either the latest version or the [**Legacy**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/tag/v.3.0) one, as it uses their Uber materials. In the case of the Legacy materials, importing any throwaway game object might be needed in order to generate the required material template if none are there.

This tool produces a simplistic glass material, Principled Shader-based, for EmissiveOnly-type materials such as those in spaceship windows, too.

As some sets of objects, such as spaceship interiors, can easily have a hundred materials or more, Blender might look like being unresponsive while processing them. Its progress can be followed in Blender's Console output, which will show the objects and materials being processed. Some error messages are prone to appear, due to some unintended interactions with the modern version of the SWTOR Importer Add-on: those are expected, and don't affect the final result.

### Deduplicate Scene's Nodegroups.
Consolidates all duplicates of a node in the scene ("node.001", "node.002", etc.) so that they become instances of the original instead of independent ones. The copies are marked as "zero users" so that, after saving the project, the next time it is opened they will be discarded (that's how Blender deals with such things).
* It acts on all the nodes of a scene, and doesn't require a selection of objects.

### Set Backface Culling On/Off.
It sets all the materials in the selected objects' Backface Culling setting to on or off (the setting is fully reversible). Many SWTOR objects, especially floors, walls, and ceilings of spaceships and some buildings, are single-sided by nature, which ought to make their sides facing away from the camera invisible. Blender, by default, renders single-sided objects as double-sided unless Backface Culling is enabled.
* It **doesn't** depend on the presence of a .gr2 importer add-on: this setting works in any kind of Blender material, no matter if SWTOR-based or any other kind.
* **The setting only acts through the Eevee renderer** (either while in Viewport Shading mode or as a final renderer). Cycles enforces double-sidedness, despite ticking the Material Properties Inspector's Backface Culling checkbox. If the intention is to do the final render through Cycles, a dual 3D Viewer setup, one in Material Preview mode (Eevee) and the other displaying the Render Preview might be the best way to finetune lighting and texturing. 

The usefulness of this tool becomes apparent when having to deal with interior scenes such as spaceship rooms, where we have to place models (characters, furniture, props.) while having the walls and ceilings occluding our view. There are cumbersome solutions to that, such as hiding polygons, playing with the camera clipping settings, or using a booleaning object to "eat" walls or ceilings away. This is simpler and faster. Also, it doesn't affect the rendering when placing the camera inside, as there the one-sided objects are facing the camera in the intended manner.

![](https://github.com/ZeroGravitasIndeed/zg_swtor_tools/blob/main/documentation/030.jpg)


**Warning: if a selected object's material is shared with objects that haven't been selected (and that's very typical in architectural objects like spaceships or buildings), the effect will be visible in those objects, too.** This is normal, and maybe inconvenient. The only solution to this would be to isolate the material we don't want to be affected by changing its name. Still, for the intended use, it doesn't seem to be anything beyond a nuisance.

## SWTOR Objects Tools:

### Quickscaler.
Scales all selected objects up or down by a factor, preserving their relative distances if their origins don't match. The idea behind the tool is to be able to quickly upscale all objects of a character or a scene to real life-like sizes (1 Blender unit = 1 m. or equivalent), as Blender requires such sizes to successfully calculate things like automatic weightmaps, physics, etc. Cameras, lights and armatures are correctly scaled, and it acts only on non-parented and parent objects, to avoid double-scaling children objects (typically, objects parented to a skeleton).

Any number between 1 and 100 can be manually entered. Recommended factors are:
* 10, for simplicity. It results in rather superheroically-sized characters.
* Around 7-8 for more realistic human heights.

### Merge Double Vertices.
Merges "duplicate" vertices (applies a "Merge By Distance" with a tolerance of 0.000001 m.), which usually solves many issues when fusing body parts or applying Subdivision or Multiresolution Modifiers.
* Requires a selection of one or several game objects.
* When selecting multiple objects, the tool acts on each of them separately so as not to merge vertices of different objects by accident.
* To correct any possible normals problems derived from the operation, it performs a face area normals' averaging operation, too.
* Also, it sets each object's Auto Smooth to On (it's typically on by default, but, just in case…).

### Modifiers Tools.
They add to all selected objects Modifiers like Subdivision or Multires (for hiding SWTOR's models' low poly nature) and Displace and Solidify (to facilitate gear-over-full body workflows), with sensible settings as an easy starting point. There is a Modifiers removal button that only affects those Modifier types, preserving any other, such as the Armature modifier that results from parenting a skeleton. Also, there are buttons for moving such Armature modifiers to the top or the bottom of the Modifier Stack, for both usefulness and experimentation.

* Requires a selection of one or several game objects.
* The Armature Modifier re-ordering buttons don't work by selecting Armature objects yet: only by selecting objects with Armature Modifiers. The former functionality will be considered for an update.

## SWTOR Misc. Tools:
For now these are simply a few already existing Blender tools that are a little too buried inside their panels and would be nice to have more at hand.

### Simplify.
Usually in the Properties Editor > Render Properties >Simplify section, it lets us temporarily switch a few common and somewhat costly options, such as Subdivision Modifiers' levels, number of particles, etc., to lower values, at the scene level. For example, we can disable subdivision while animating a character, which will make its meshes react to our posing far faster.

### Pose Position / Rest Position.
It shows the Pose Position and Rest Position buttons that appear at the Properties Editor > Object Properties, Skeleton section when a skeleton is selected, letting us quickly alternate between those two states. It only acts on the Active armature (the Active Object that happens to be an armature at the moment) instead of all selected armatures. Having it act on all of them is in the works.

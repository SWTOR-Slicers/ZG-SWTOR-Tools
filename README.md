# ZeroGravitas' SWTOR Tools.

This Blender Add-on provides with a miscellanea of tools to use on **Star Wars: The Old Republic**'s game assets, including an Uber Materials Processor for static game models. It will grow in features as new ideas come up. Quality of code-wise, "this is not a place of honor": It Just (Hardly) Works™.

* [Installation.](#installation)
* [Materials Tools:](#swtor-materials-tools)
  * [Process Uber Materials.](#process-uber-materials)
  * [**NEW!** Custom SWTOR Shaders (beta):](#custom-swtor-shaders)
	  * [Add Custom SWTOR Shaders.](#add-custom-swtor-shaders)
	  * [Convert to Custom SWTOR Shaders.](#convert-to-custom-swtor-shaders)
	  * [About the included Custom Shaders.](#about-the-included-custom-shaders)
	  * [Custom Shaders' Extras.](#custom-shader-extras)
	  * [About the current Beta state.](#about-the-beta-state)
  * [Deduplicate Scene's Nodegroups.](#deduplicate-scenes-nodegroups)
  * [Set Backface Culling On/Off.](#set-backface-culling-onoff)
* [Objects Tools:](#swtor-objects-tools)
  * [Quickscaler.](#quickscaler)
  * [Merge Double Vertices.](#merge-double-vertices)
  * [Modifiers Tools.](#modifiers-tools)
* [Misc. Tools:](#swtor-misc-tools)
  * [Set all .dds to Raw/Packed.](#set-all-dds-to-rawpacked)
  * [Simplify Scene.](#simplify)
  * [Switch Skeleton between Pose and Rest Position.](#pose-position--rest-position)
  * [Camera to View.](#camera-to-view)


## Installation:

The installation of the Add-on in Blender follows the usual directions:

1. [**Download the Add-on's "zg_swtors_tool.zip" file from this link**](/zg_swtor_tools.zip). Don't unZip it: it's used as such .zip.
2. [**Download the "custom_swtor_shaders.zip" file from this link**](/custom_swtor_shaders.zip). UnZip this one and keep the resulting Blender file somewhere in handy. **This file is only necessary if we intend to play with the Custom SWTOR Shaders tools, currently in beta**.
3. In Blender, go to Edit menu > Preferences option > Add-ons tab > Install… button.
4. Select the Add-on in the file dialog box and click on the Install Add-on button.
5. The Add-on will appear in the Add-ons list with its checkbox un-ticked. Tick it to enable the Add-on.
6. Twirl the arrow preceding the check-box to reveal some information and, most importantly, **the Add-on's Preference settings**. Filling those is crucial for some of the tools to work correctly. They are:

	![](/images/zg_010.png)
	* **Path of a "resources" folder**: some of the Add-on's features depend on looking for information and game assets inside a SWTOR assets extraction (typically produced by apps such as SWTOR Slicers or EasyMYP). In the case of a SWTOR Slicers extraction, the "resources" folder is inside the folder set as that app's Output Folder.
	
		Click on the folder icon to produce a file browser dialog window where to locate the "resources" folder, or type or copy its path inside the folderpath field.
		
	* **Path to a Custom Shaders .blend file (if any)**: only required by a couple of tools that allow us to replace the current .gr2 Add-on's modern SWTOR shaders with custom ones held in one Blender file, meant for us to experiment with and improve upon. See: [Custom SWTOR Shaders (beta)](#custom-swtor-shaders). 

		Click on the file icon to produce a file browser dialog window where to select such a Blender project file, like the one linked in the second step of the installation instructions, or type or copy its path inside the filepath field.
        
The Add-on's tools will appear in the 3D Viewport's Sidebar ('n' key), in the "ZG SWTOR" tab.

![](/images/zg_020.png)

The current tools are:

## SWTOR Materials Tools:

### Process Uber Materials.
![](/images/zg_ui_010.png)

**Requirements:**
* **Selecting a "resources" folder in this Add-on's preferences settings.**
* **An enabled SWTOR .gr2 Add-on, be it the Legacy Add-on or the current modern one.**
* **A selection of objects.**

This tool processes all the Uber-type materials detected in a selection of objects, locating their related texturemaps and linking them to a SWTOR Uber shader (modern or legacy, whichever is active). It processes any EmissiveOnly-type (glass) materials, too. It's particularly fast, as it (only) works with an asset extraction's "resources" folder.

Options:
* **Overwrite Uber Materials** (off by default): overwrites already present Uber and EmissiveOnly objects's materials, which allows for regenerating materials that might have lost texturemaps, for converting Uber materials from Legacy to modern and viceversa, etc.
* **Collect Collider Objects** (on by default): adds all objects with an "Util_collision_hidden" material type or texturemap to a Collection named "Collider Objects".

**It needs the presence of an enabled [SWTOR importer Add-on ("io_scene_gr2")](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x)** in Blender, either the latest version or the [**Legacy**](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/tag/v.3.0) one, as it uses their Uber materials. In the case of the Legacy materials, importing any throwaway game object might be needed in order to generate the required material template if none are there.

This tool also produces a simplistic glass material, Principled Shader-based, for EmissiveOnly-type materials such as those in spaceship windows.

As some sets of objects, such as spaceship interiors, can easily have a hundred materials or more, Blender might look like being unresponsive while processing them. Its progress can be followed in Blender's Console output, which will show the objects and materials being processed. Some error messages are prone to appear in the console, due to some unintended interactions with the modern version of the SWTOR Importer Add-on: those are expected, and don't affect the final result.

**If a selected object's material is shared with objects that haven't been selected** (and that's very typical in architectural objects like spaceships or buildings) **they'll show those processed materials, too, as if they would have been included in the selection.** This is their expected behavior. If needed, the way to avoid this would be to isolate the material we don't want to be processed by changing its name to one that doesn't exist in SWTOR's shaders folder.

### Custom SWTOR Shaders.
![](/images/zg_ui_020.png)

**THIS FEATURE IS IN A BETA STAGE. It shouldn't break anything but itself at its worst, though.**

**Requirements:**

* **Blender 3.x** (Blender 2.8x-9.x support coming soon).
* **Selecting a custom SWTOR shaders-holding .blend file in this Add-on's preferences settings.**
* **An enabled latest version of the SWTOR .gr2 Add-on, only needed at the very moment this tool is being used (supporting the Legacy one is being considered).**
* **A selection of objects.**

As convenient as our modern, *smart* SWTOR shaders for Blender are, especially for the novice (no dangling texturemap nodes, not having to manually adjust Material or texturemap images' settings, no risk of overwriting template materials), they are a little harder to customize than the previous, now Legacy ones. Both versions, being generated programmatically (the .gr2 Add-ons' code produce them on the fly while importing SWTOR object files), are harder to customize in a reusable manner, too: most modifications can be done once applied to objects, but those modifications have to be redone or copied (if feasible) between projects.

So, what we've done here is two things:

* We've "dumbed down" the modern shaders: no smarts, the texturemap nodes are back to dangling from the SWTOR Shader nodegroups (so allowing to interpose color correction nodes and stuff as usual), no automatic adjustment of texturemap images and materials' settings (although the converter tool has that sorted).
* Instead of having an Add-on code generate the shaders on the fly, the shaders are stored in a .blend file, and the Add-on replaces the normal modern shaders with these dumb ones, placing the involved texturemaps' nodes alongside and linking them correctly.

What are the advantages to this?

* The most important one is that any modifications to this SWTOR shaders "library" Blender file can be tried and saved quickly just by playing in that Blender project. What's more: if we choose to have the Add-on replace the modern shaders in a given object with these dumb ones by **linking** to them instead of **appending** them, any improvement done to the shaders in the future will become available to older projects using linked shaders automatically. And if we need to do a per-project custom work, we can always convert a linked shader into a permanent one (with Blender's Make Local option).
* **These customizable shaders can coexist with the modern, automated ones**. What's more: one can keep both in a given material and alternate linking them to the Material Output node for comparison sake (or by putting a Mix Shader in-between) or as a backup of sorts.
* We can even maintain several differentiated SWTOR shader library files at once, to try different approaches without compromising previous projects. As the data on where each linked shader comes from is stored in the Blender projects using them, we can keep several library files with different names and just set the one we want to link to or append from in any given moment in the Add-on's preference settings. Some care would be needed, such as not moving those library files around or we will have to reconnect them, and maybe keeping a sensible naming scheme. Just the usual)
* Finally: this setup makes comparing notes extremely easy, just by sharing our library .blend files between fellow hobbyists.

So, how does this work on a practical level? The available tools are:

#### Add Custom SWTOR Shaders:
This tool is only needed if we want to add the shaders to a Blender project that has no previously textured SWTOR objects we could just convert. It simply adds them to the currently open Blender project: they'll become available through add > Group submenu (the ones in the add > SWTOR submenu are the usual modern shaders, instead). This tool is disabled if we happen to be editing the .blend file we selected as a library in the Add-on's preference settings, to avoid accidental duplications or loopbacks. Its options are:

* **Link instead of Append**: as explained, Append adds a fully modifiable copy of the shaders. Link, instead, inserts instances of the shaders stored in the library .blend project. We can adjust their settings normally, but we won't be able to modify the nodes inside their nodegroups. There are ways to edit both the library and the working project at once, by using two instances of Blender, each opening each file, and saving-and-reverting the working project every time we save a change in the library one.

	This option is on by default except when editing a library file, in which case it wouldn't make sense to use linking.

#### Convert to Custom SWTOR Shaders:
**Doesn't require to previously use the Add Custom SWTOR Shaders: it does that by itself.**

It goes through all the materials in a selection of objects, detects the presence of the modern SWTOR shaders, and inserts the customizable versions with the same settings plus the needed texturemap nodes. Its options are:

* **Link instead of Append**: it works exactly like in the previous tool.
* **Preserve Original Shaders**: it doesn't delete the original modern shaders, simply pushing them aside inside the material, unlinked. If anything were to go wrong sometime further on in our experimentations, we can always unlink the customizable ones and relink the originals. This option is on by default.

	![](/images/zg_040.png)

We can regenerate the customizable shader in a material by deleting it and its texturemaps and Converting the material again, as long as the original shader still exists in it. That's why preserving them is on by default.

#### About the included custom shaders:
Alongside this Add-on's .zip file, there comes a sample .blend file holding just the customizable shaders. It can be renamed and stored wherever however and wherever we want, although we should decide a stable location for it and its derivatives, as moving it somewhere else after being applied in linked mode would lead to having to tell each Blender project using it where it was been moved to.

The only rule for the [**Convert to Custom SWTOR Shaders**](#convert-to-custom-swtor-shaders) tool not to fail is to keep the names of the shaders intact. These are:

* SWTOR - Uber
* SWTOR - Creature
* SWTOR - Garment
* SWTOR - SkinB
* SWTOR - Eye
* SWTOR - HairC

All the auxiliary custom shaders inside their nodegroups have been renamed by adding a "SW Aux - " prefix (e.g.: "SW Aux - ManipulateHSL"). Such renaming helps us avoid conflicts with the original .gr2 Add-on's own shaders, as we might want to modify the auxiliary shaders, too (some are already modified). Strictly speaking, in the case of these auxiliary shaders, they only need to have different names to the originals. it's in the main ones' case where we need to keep the names stated above.

These shader library Blender projects don't need to be kept empty of objects and texturemaps. Actually, the most convenient thing to do would be to populate them with objects representative of the shaders' usage, so that we can try stuff on them. Say, some ship interiors for the Uber shader; some animals for the Creature one; Player Characters of diverse species for SkinB, HairC and Eye, some armor sets for the Garment shader… We haven't pre-populated the downloadable sample project in this repository because of both copyright-related reasons and file sizes.

#### Custom Shader Extras:
Just as a first example of adding custom stuff to the shaders, the ones included in the .blend file come with a few extras already, not just in their inputs and settings but in their outputs, too. They are rather tentative and far from perfect, mostly a suggestion of what can be done.

![](/images/zg_050.png)

Extra Inputs:
* **Specular and Roughness strength**: they try to simulate the Principled BSDF shader's settings of the same name.
* **Emission Strength**: for turning control panels, capital ship windows, gear's glowy bits and others decidedly incandescent! 
* **Normal Strength**: raised above 1.0, it emphasizes objects's surface relief, if in a somewhat wonky way. It doesn't work terribly great on solid surface objects, but in characters it provides a very striking "**League of Legends: Arcane**" look (which in the series was achieved through hand-painted textures), so, we suspect it's going to be a favorite.
* **Transparency**: this is a global material transparency factor, unrelated to its opacity map. Its main mission is to allow us to invisibilize a part of an object, such as the feet of a Player Character that has been turned into a single mesh and happens to be poking through its boots.
* **Complexion Gamma**: to contrast a character's complexion texturemap without the need to switch its Color Space to sRGB or interpose some color correction node.
* **Scar Gamma, Color and Normal Strength**, to adjust scars and age maps just the way we want them.
* **Direction Map**: it's been added to the SkinB shader in a provisional manner (I'm not sure if it's correctly done).

Not everything works well: the ones in the Eye Shader hardly show any effect and need rethinking (also, we need Sith Glowy Eyes. Coming soon :D ). DirectionMaps seem to get extremely wonky in some objects when rendering through Cycles, too.

Extra Outputs:
* **Diffuse Color AUX**: the diffuse color in RGB, with the PaletteMap re-hue already applied!
* **Specular Color AUX**: the specular color on black, in RGB. Typically, one would mix it with the diffuse in Add mode.
* **Emission Strength AUX**: it's the emissive channel from the _n RotationMap.
* **Alpha AUX**: it's the opacity channel from the _n RotationMap.
* **Normal AUX**: this is the Normal information, already processed to be directly usable in any Blender node that we could want to chain to the rest of the shader's outputs.

These channels are mostly there for experimenting with adding our own node trees for things like, say, trying comic book or anime-like Non Photorealistic Rendering (NPR), or maybe to produce baking information.

* **DirectionMap Vector**: as DirectionMaps (a kind of anisotropic glossmap used in hairs, some species' furs and skins, and other cases such as weapons' metallic surfaces) require pre-calculated data that is internally generated in the automatic modern shaders, this is a bit of a cludgey way to produce that information and link it to the DirectionMaps' vector input. The Converter tool adds those links by itself.

#### About the beta state:
The Add-on, as it is now, needs work in things like failing gracefully to errors, providing support for older Blender and .gr2 add-on versions, refining the existing extra features (for example, per dye area-Spec/Rough/Emissive/Normal strength settings), and most probably rearranging the shaders' node trees into something a bit more wieldable.

That said, we should point out that these shaders, as such, are meant to be further customized and evolved by any of us based on our particular interests. For example, the current implementation of glossiness is meant to replicate SWTOR's own, but someone might prefer to discard that and do their own Blender Specular node or Principled BSDF node-based one, or substitute SWTOR's Flush Tone-based pseudo-subsurface scattering effect with Blender's own, add adjustable noise-based skin pores, etc.

The downloadable shader library file is just an example of a starting point. The sky is the limit.



### Deduplicate Scene's Nodegroups.
![](/images/zg_ui_030.png)

**Requirements: none.**

Consolidates all duplicates of a node in the scene ("node.001", "node.002", etc.) so that they become instances of the original instead of independent ones. The copies are marked as "zero users" so that, after saving the project, the next time it is opened they will be discarded (that's how Blender deals with such things).
* It acts on all the nodes of a scene, so, it doesn't require a selection of objects.

### Set Backface Culling On/Off.
![](/images/zg_ui_040.png)

**Requirements: use Eevee in the 3D viewport for the effect to be visible.**

It sets all the materials in the selected objects' Backface Culling setting to on or off (the setting is fully reversible). Many SWTOR objects, especially floors, walls, and ceilings of spaceships and some buildings, are single-sided by nature, which ought to make their sides facing away from the camera invisible. Blender, by default, renders single-sided objects as double-sided unless Backface Culling is enabled.
* It **doesn't** depend on the presence of a .gr2 importer Add-on: this setting works in any kind of Blender material, no matter if SWTOR-based or any other kind.
* **The setting only acts through the Eevee renderer** (either while in Viewport Shading mode or as a final renderer). Cycles enforces double-sidedness, no matter if we tick the Material Properties Inspector's Backface Culling checkbox. If the intention is to do the final render through Cycles, a dual 3D Viewer setup, one in Material Preview mode (Eevee) and the other displaying the Render Preview might be the best way to finetune lighting and texturing. 

The usefulness of this tool becomes apparent when having to deal with interior scenes such as spaceship rooms, where we have to place models (characters, furniture, props.) while having the walls and ceilings occluding our view. There are cumbersome solutions to that, such as hiding polygons, playing with the camera clipping settings, or using a booleaning object to "eat" walls or ceilings away. This is simpler and faster. Also, it doesn't affect the rendering when placing the camera inside, as in there the one-sided objects are facing the camera in the intended manner.

![](/images/zg_030.jpg)

When assembling multi-object locations, it's typical that a same material is shared between several objects. That can lead to unselected objects showing the effects of this tool as if they would have been included in the selection. This is an expected behavior. The only way to avoid this would be to isolate the material we don't want to be affected by changing its name.

## SWTOR Objects Tools:

### Quickscaler.
![](/images/zg_ui_050.png)

**Requirements: a selection of objects.**

Scales all selected objects up or down by a factor, preserving their relative distances if their origins don't match. The idea behind the tool is to be able to quickly upscale all objects of a character or a scene to real life-like sizes (1 Blender unit = 1 m. or equivalent), as Blender requires such sizes to successfully calculate things like automatic weightmaps, physics simulations, etc.

**Cameras, lights and armatures are correctly scaled, and it acts only on non-parented and parent objects**, to avoid double-scaling children objects (typically, objects parented to a skeleton). **Objects set as insensitive to selection operations in the Outliner aren't affected by this tool**.

Any number between 1 and 100 can be manually entered. Recommended factors are:
* 10, for simplicity. It results in rather superheroically-sized characters.
* Around 7-8 for more realistic human heights.

### Merge Double Vertices.
![](/images/zg_ui_060.png)

**Requirements: a selection of objects.**

Merges "duplicate" vertices (applies a "Merge By Distance" with a tolerance of 0.000001 m.), which usually solves many issues when fusing body parts or applying Subdivision or Multiresolution Modifiers to any SWTOR object.
* Requires a selection of one or several game objects.
* When selecting multiple objects, the tool acts on each of them separately so as not to merge vertices of different objects by accident.
* To correct any possible normals problems derived from the operation, it performs a face area normals' averaging operation, too.
* Also, it sets each object's Auto Smooth to On (it's typically on by default, but, just in case…).
If we intend to subdivide objects such as weapons or some bits of armor that happen to be very simplistic, we suggest to test that subdividing immediately after merging doubles to check that there won't be problems that require additional massaging. That, or keeping non-merged duplicates of the objects, just in case we have to backtrack. 

### Modifiers Tools.
![](/images/zg_ui_070.png)

**Requirements: a selection of objects.**

They add to all selected objects Modifiers like Subdivision or Multires (for hiding SWTOR's models' low poly nature) and Displace and Solidify (to facilitate gear-over-full body workflows), with sensible settings as an easy starting point. There is a Modifiers removal button that only affects those Modifier types, preserving any other, such as the Armature modifier that results from parenting a skeleton. Also, there are buttons for moving such Armature modifiers to the top or the bottom of the Modifier Stack, for both usefulness and experimentation.

* Requires a selection of one or several game objects.
* The Armature Modifier re-ordering buttons don't work by selecting Armature objects yet: only by selecting objects that have received Armature Modifiers. The former functionality will be considered for an update.

## SWTOR Misc. Tools:
Minor tools. Most of those these are simply a few already existing Blender tools that are a little too buried inside their panels and would be nice to have more at hand.

### Set all .dds to Raw/Packed.
![](/images/zg_ui_080.png)

**Requirements: none.**

It sets all images in the blender project whose names end with the .dds extension (as is the case in SWTOR's texturemap images) to Color Space: Raw, and Alpha: Channel Packed, which are the settings our SWTOR shaders expect in order to work properly.
* It acts on all the images of a scene, so, doesn't require a selection of objects.

(It's typical to set some texturemap images, such as complexion maps, to sRGB because that makes them appear a little bit darker, something that this tool would revert. Such trick should be no longer necessary by using the new customizable shaders' extra Complexion Gamma settings).

### Simplify.
![](/images/zg_ui_090.png)

**Requirements: none.**

Already available in the Properties Editor > Render Properties > Simplify section, this tool lets us temporarily switch a few common and somewhat costly options, such as Subdivision Modifiers' levels, number of particles, etc., to lower values, at the scene level. For example, we can disable subdivision while animating a character, which will make its meshes react to our posing far faster.

### Pose Position / Rest Position.
![](/images/zg_ui_090.png)

**Requirements: a selection of objects including an armature.**

It shows the Pose Position and Rest Position buttons already available at the Properties Editor > Object Properties > Skeleton section when a skeleton is selected, letting us quickly alternate between those two states. It only acts on the Active armature (the Active Object that happens to be an armature at the moment) instead of all selected armatures. Having it act on all of them is in the works.

### Camera to View.
![](/images/zg_ui_090.png)

**Requirements: none.**

Same checkbox as the options panel's View Tab > View Lock section > Lock Camera to View, for easily switching from framing the scene from the camera POV to keeping the camera unaffected while navigating the viewport.

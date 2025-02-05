# For references to approaches to the subject, see:
# https://blender.stackexchange.com/questions/45992/how-to-remove-duplicated-node-groups
# https://gist.github.com/IPv6/0886731e6e98b6968cb1ffa0b8d5900e
# https://meshlogic.github.io/posts/blender/scripting/eliminate-material-duplicates/ (the one used here)

import bpy
import hashlib
import struct
import re
import datetime
import time  # Import for timing

# region (attempts at using hashing. Not working yet)

# def duplicate_and_delete_image(image_name):
#     # Get the image by name
#     source_image = bpy.data.images.get(image_name)
#     if not source_image:
#         print(f"Image '{image_name}' not found in bpy.data.images.")
#         return

#     # Generate a unique name based on the current date and time
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     new_image_name = f"Duplicate_{timestamp}"

#     # Start the timer
#     start_time = time.perf_counter()

#     # Create a new image with the same dimensions and color data
#     duplicate_image = bpy.data.images.new(
#         name=new_image_name,
#         width=source_image.size[0],
#         height=source_image.size[1],
#         alpha=source_image.use_alpha  # Preserve alpha channel if present
#     )

#     # Copy pixel data directly
#     duplicate_image.pixels[:] = source_image.pixels[:]

#     # End the timer for duplication
#     duplication_time = time.perf_counter() - start_time
#     print(f"Duplicate image created in {duplication_time:.6f} seconds: {new_image_name}")

#     # Start the timer for deletion
#     delete_start_time = time.perf_counter()

#     # Delete the duplicate image
#     bpy.data.images.remove(duplicate_image)

#     # End the timer for deletion
#     deletion_time = time.perf_counter() - delete_start_time
#     print(f"Duplicate image deleted in {deletion_time:.6f} seconds: {new_image_name}")

#     # Total time
#     total_time = duplication_time + deletion_time
#     print(f"Total operation time: {total_time:.6f} seconds")

# def hash_image_content_int(image_name: str, resolution: tuple = (8, 8)) -> str:
#     """
#     Hash the content of an image, including the alpha channel, by resizing it
#     to a low resolution and calculating its MD5 hash using only standard Python modules.

#     :param image_name: The name of the image loaded in Blender.
#     :param resolution: The resolution to resize the image to (default is 8x8).
#     :return: The MD5 hash of the image content (including alpha).
#     """
#     # Get the image from Blender's data
#     image = bpy.data.images.get(image_name)
#     if not image:
#         raise ValueError(f"Image '{image_name}' not found in Blender data.")

#     # Ensure the image has pixels loaded
#     if not image.has_data:
#         raise ValueError(f"Image '{image_name}' does not have pixel data loaded.")

#     # Prepare a new temporary image for resizing
#     # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     # new_image_name = f"Duplicate_{timestamp}"

#     temp_image_name = f"temp_to_hash-{image_name}"
#     if temp_image_name in bpy.data.images:
#         bpy.data.images.remove(bpy.data.images[temp_image_name])

#     # Create a new image at the desired resolution
#     temp_image = bpy.data.images.new(temp_image_name, width=resolution[0], height=resolution[1])

#     # Copy the original image's data into the temporary image
#     temp_image.scale(resolution[0], resolution[1])

#     # Extract the resized image's pixel data
#     resized_pixels = temp_image.pixels[:]
#     bpy.data.images.remove(temp_image)  # Cleanup temporary image

#     # Convert the pixel data to a byte array (RGBA)
#     pixel_data = bytearray()
#     for i in range(0, len(resized_pixels), 4):  # Iterate over RGBA in steps of 4
#         r, g, b, a = resized_pixels[i:i+4]
#         pixel_data.extend(struct.pack("BBBB",
#                                       int(r * 255),
#                                       int(g * 255),
#                                       int(b * 255),
#                                       int(a * 255)))

#     # Compute the MD5 hash of the byte array
#     md5_hash = hashlib.md5(pixel_data).hexdigest()
    
#     return md5_hash

# def hash_image_content_float(image_name: str, resolution: tuple = (8, 8)) -> str:
#     """
#     Hash the content of an image using floating-point pixel values.
#     """
#     image = bpy.data.images.get(image_name)
#     if not image or not image.has_data:
#         raise ValueError(f"Image '{image_name}' is not available or lacks pixel data.")
    
#     temp_image_name = f"{image_name}_resized"
#     if temp_image_name in bpy.data.images:
#         bpy.data.images.remove(bpy.data.images[temp_image_name])
    
#     temp_image = bpy.data.images.new(temp_image_name, width=resolution[0], height=resolution[1])
#     temp_image.scale(resolution[0], resolution[1])
#     resized_pixels = temp_image.pixels[:]
#     bpy.data.images.remove(temp_image)
    
#     pixel_data = bytearray()
#     for i in range(0, len(resized_pixels), 4):
#         r, g, b, a = resized_pixels[i:i+4]
#         pixel_data.extend(struct.pack("ffff", r, g, b, a))
    
#     return hashlib.md5(pixel_data).hexdigest()

# def deduplicate_images_by_hash():
#     """
#     Deduplicate images in Blender based on image hashes.
#     Remaps users of duplicate images to the deduplicated one.
#     """
#     # Dictionary to track unique base names and their associated image
#     unique_images = {}

#     # List to hold images to remove later
#     images_to_remove = []

#     for image in bpy.data.images:
        
#         image_hash = hash_image_content_int(image.name)
#         print(f"{image.name} - {image_hash}")

#         if image_hash not in unique_images:
#             unique_images[image_hash] = image  # Keep this as the master copy
#         else:
#             # Duplicate detected
#             master_image = unique_images[image_hash]
#             print(f"Duplicate found: {image.name} (remapping to {master_image.name})")

#             # Remap users to the master image
#             image.user_remap(master_image)

#             # Schedule the duplicate image for removal
#             images_to_remove.append(image)

#     # Remove duplicate images
#     img_count_report = 0
#     for image in list(images_to_remove):  # we duplicate list to avoid deleted refs issues
#         # Ensure no users are linked to this image before removal
#         if image.users == 0:
#             image_name = image.name
#             bpy.data.images.remove(image)
#             print(f"Removed duplicate image: {image_name}")
#             img_count_report += 1
#         else:
#             print(f"Cannot remove {image.name} - still has users!")

#     print("Deduplication and remapping complete!")

#     return img_count_report

# endregion



def deduplicate_images_by_name_and_size():
    """
    Deduplicate images in Blender based on name suffixes (_001, .001, etc.).
    Remaps users of duplicate images to the deduplicated one.
    """
    # Regular expression to match suffixes (e.g., _001, .001, -001, etc.)
    suffix_pattern = re.compile(r'(.+?)([-_.]?\d+)$')

    # Dictionary to track unique base names and their associated image
    unique_images = {}

    # List to hold images to remove later
    images_to_remove = []

    print("===================")
    print("IMAGES DEDUPLICATOR")
    print("Names & sizes-based")
    print("===================")
    
    print()
    print("DETECTING AND REMAPPING DUPLICATES")
    print("----------------------------------")
    print()


    for image in bpy.data.images:
        # Match image name to detect suffix
        match = suffix_pattern.match(image.name)
        if match:
            base_name = match.group(1)  # Extract base name without suffix
        else:
            base_name = image.name  # No suffix; use the full name

        # Check if this base name is already in the dictionary
        if base_name not in unique_images:
            unique_images[base_name] = image  # Keep this as the master copy
        else:
            # Duplicate detected
            master_image = unique_images[base_name]
            # Check that image dimensions match, to prevent accidental dedupe
            # of modernized image assets post Game Update 7.6 otherwise
            if image.size[:] == master_image.size[:]:
                print(f"Duplicate found:  {image.name}  -  Remapping to:  {master_image.name}")

                # Remap users to the master image
                image.user_remap(master_image)

                # Schedule the duplicate image for removal
                images_to_remove.append(image)
            else:
                print()
                print(f"--- Duplicate omitted:  {image.name} has a size difference to  {master_image.name}")
                print()

    # Remove duplicate images
    
    print()
    print()
    print("REMOVING DUPLICATES")
    print("-------------------")
    print()

    img_count_report = 0
    for image in list(images_to_remove):  # we duplicate list to avoid deleted refs issues
        # Ensure no users are linked to this image before removal
        if image.users == 0:
            image_name = image.name
            bpy.data.images.remove(image)
            print(f"Removed:  {image_name}")
            img_count_report += 1
        else:
            print(f"--- Cannot remove:  {image.name} - still has users!")

    print()
    print("DEDUPLICATION AND REMAPPING COMPLETE!")
    print()
            
    return img_count_report






class ZGSWTOR_OT_deduplicate_images(bpy.types.Operator):

    bl_idname = "zgswtor.deduplicate_images"
    bl_label = "ZG Deduplicate Images"
    bl_description = "Replaces all images whose names end with numbered suffixes\n(.001, .002, etc.) with instances of a non-suffixed original.\n\nThis operator affects all images in the current Scene\nand doesn't require a selection"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls,context):
        if bpy.data.images:
            return True
        else:
            return False


    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        duplicates_amount_report = deduplicate_images_by_name_and_size()
        
        bpy.context.window.cursor_set("DEFAULT")
        self.report({'INFO'}, str(duplicates_amount_report) + " duplicate images deduped and set to zero users" )
        return {'FINISHED'}


# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_deduplicate_images)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_deduplicate_images)

if __name__ == "__main__":
    register()
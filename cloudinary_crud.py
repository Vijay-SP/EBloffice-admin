import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="ebl-offices",
    api_key="531292511735253",
    api_secret="wkFaVJfN_6Bg3RqxVbY4slFz2eo",
    secure=True
)

property_preset = "properties_img_store"
floor_plan_preset = "floor_plan_img_store"


def uploadSinglePropertyImage(file):
    return cloudinary.uploader.upload(
        file, upload_preset=property_preset)


def uploadSingleFloorPlanImage(file):
    return cloudinary.uploader.upload(
        file, upload_preset=floor_plan_preset)


def uploadPropertyImages(request):
    file_list = request.files.getlist("prop-files[]")
    file_ref = []
    for file in file_list:
        upload_result = uploadSinglePropertyImage(file)
        file_ref.append(upload_result["url"])
    return file_ref


def uploadFloorPlanImages(request):
    file_list = request.files.getlist("floor-plan-files[]")
    file_ref = []
    for file in file_list:
        upload_result = uploadSingleFloorPlanImage(file)
        file_ref.append(upload_result["url"])
    return file_ref


def deleteFloorPlanImages(img_links):
    for link in img_links:
        splitted = link.split('/')
        public_id = splitted[len(splitted)-1].split(".")[0]
        delete_response = cloudinary.uploader.destroy(
            "floor_plan_images/" + public_id, invalidate=True, resource_type="image")


def deletePropertyImages(img_links):
    for link in img_links:
        splitted = link.split('/')
        public_id = splitted[len(splitted)-1].split(".")[0]
        delete_response = cloudinary.uploader.destroy(
            "properties_images/" + public_id, invalidate=True, resource_type="image")

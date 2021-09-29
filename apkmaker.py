from os_android_apk_builder.objs.KeyStoreProperties import KeyStoreProperties
from os_android_app_version_changer.objs.VersionProperties import VersionProperties
from os_android_apk_builder import apk_builder


def make_apk(project_path=None,
				apk_destination_path=None,
				keystore_path=None,
				key_alias=None,
				key_password=None,
				store_password=None):
	# Setting KeyStore properties
	key_store_props = KeyStoreProperties(key_store_file_path=keystore_path,
											store_password=store_password,
											key_alias=key_alias,
											key_password=key_password,
											v1_signing_enabled=True,
											v2_signing_enabled=True)

	# Setting the version properties (version code and version name)
	version_props = VersionProperties(new_version_code=VersionProperties.RAISE_VERSION_BY_ONE,
										new_version_name="1.0.3")

	# Building APK
	apk_builder.build_apk(project_path=project_path,
							apk_dst_dir_path=apk_destination_path,
							key_store_properties=key_store_props,
							version_properties=version_props)
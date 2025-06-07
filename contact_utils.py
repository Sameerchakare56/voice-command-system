import kivy
from kivy.utils import platform
from difflib import SequenceMatcher

ANDROID = platform == 'android'
if ANDROID:
    try:
        from jnius import autoclass, cast
        # Only import android.permissions on Android
        from android.permissions import request_permissions, Permission
    except ImportError:
        print("Android modules not available")
        ANDROID = False

def similar(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_contact_number_by_name(name):
    if not ANDROID:
        print("Contact lookup is only available on Android")
        return None

    try:
        # Request contacts permission only on Android
        if ANDROID:
            request_permissions([Permission.READ_CONTACTS])
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        ContentResolver = activity.getContentResolver()

        ContactsContract_Contacts = autoclass('android.provider.ContactsContract$Contacts')
        ContactsContract_CommonDataKinds_Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')

        uri = ContactsContract_Contacts.CONTENT_URI
        cursor = ContentResolver.query(uri, None, None, None, None)

        best_match = None
        best_similarity = 0.6  # Minimum similarity threshold (0.0 to 1.0)
        best_contact_name = None

        if cursor:
            while cursor.moveToNext():
                name_index = cursor.getColumnIndex(ContactsContract_Contacts.DISPLAY_NAME)
                contact_name = cursor.getString(name_index)
                
                # Calculate similarity between spoken name and contact name
                similarity = similar(name, contact_name)
                print(f"Checking contact: {contact_name}, Similarity: {similarity:.2f}") # Debug print
                
                # If this is a better match than what we've found so far
                if similarity > best_similarity:
                    contact_id_index = cursor.getColumnIndex(ContactsContract_Contacts._ID)
                    contact_id = cursor.getString(contact_id_index)

                    # Get phone number for this contact
                    phone_uri = ContactsContract_CommonDataKinds_Phone.CONTENT_URI
                    phone_cursor = ContentResolver.query(
                        phone_uri, None,
                        ContactsContract_CommonDataKinds_Phone.CONTACT_ID + " = ?",
                        [contact_id], None
                    )

                    if phone_cursor and phone_cursor.moveToFirst():
                        number_index = phone_cursor.getColumnIndex(ContactsContract_CommonDataKinds_Phone.NUMBER)
                        number = phone_cursor.getString(number_index)
                        best_match = number
                        best_similarity = similarity
                        best_contact_name = contact_name
                        phone_cursor.close()
                    if phone_cursor:
                        phone_cursor.close()
            cursor.close()
        
        if best_match:
            print(f"Found match: {best_contact_name} (similarity: {best_similarity:.2f})")
            return best_match
        return None
    except Exception as e:
        print(f"Error accessing contacts: {e}")
        return None 
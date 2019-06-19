define({ "api": [
  {
    "type": "POST",
    "url": "/accounts/add_set",
    "title": "Add set",
    "description": "<p>Make an copy of an existing character set in user's library</p>",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "set_id",
            "description": "<p>the id of the set to be added</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 400": [
          {
            "group": "Error 400",
            "type": "String",
            "optional": false,
            "field": "msg",
            "description": "<p>the detail of the exception</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsAdd_set"
  },
  {
    "type": "POST",
    "url": "/accounts/delete_character",
    "title": "Delete character",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "character_id",
            "description": "<p>the Jiezi id of the character</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "set_id",
            "description": "<p>(optional) the id of the user set for the character to be deleted from, otherwise the character will be delete from all user sets of the current user</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsDelete_character"
  },
  {
    "type": "POST",
    "url": "/accounts/delete_set",
    "title": "Delete set",
    "description": "<p>Delete a user set</p>",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "set_id",
            "description": "<p>the id of the user set to be deleted from</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "is_delete_characters",
            "defaultValue": "False",
            "description": "<p>(optional) false will not delete the characters in this set from the user library, even if they don't belong to any sets</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsDelete_set"
  },
  {
    "type": "POST",
    "url": "/accounts/get_available_sets",
    "title": "Get available sets",
    "description": "<p>Get available existing character sets to add</p>",
    "group": "accounts",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "sets",
            "description": "<p>list of serialized UserCharacterTag objects</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsGet_available_sets"
  },
  {
    "type": "POST",
    "url": "/accounts/rename_set",
    "title": "Rename set",
    "description": "<p>Rename a user set</p>",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "set_id",
            "description": "<p>the id of the user set to change name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_name",
            "description": "<p>this cannot be the same as the name of a current set</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsRename_set"
  },
  {
    "type": "POST",
    "url": "/search",
    "title": "Search (not finished)",
    "description": "<p>search using a given keyword</p>",
    "group": "general",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "key_word",
            "description": "<p>the keyword to be searched</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "characters",
            "description": ""
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "accounts/views.py",
    "groupTitle": "general",
    "name": "PostSearch"
  }
] });

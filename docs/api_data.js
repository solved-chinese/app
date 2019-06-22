define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "Jiezi/docs/main.js",
    "group": "_media_share_Jiezi_docs_main_js",
    "groupTitle": "_media_share_Jiezi_docs_main_js",
    "name": ""
  },
  {
    "type": "POST",
    "url": "/accounts/add_set/",
    "title": "Add set",
    "description": "<p>Make an copy of an existing character set in user's library</p>",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
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
    "filename": "Jiezi/accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsAdd_set"
  },
  {
    "type": "POST",
    "url": "/accounts/delete_character/",
    "title": "Delete character",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "character_id",
            "description": "<p>the Jiezi id of the character</p>"
          },
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "set_id",
            "description": "<p>(optional) the id of the user set for the character to be deleted from, otherwise the character will be delete from all user sets of the current user</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "Jiezi/accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsDelete_character"
  },
  {
    "type": "POST",
    "url": "/accounts/delete_set/",
    "title": "Delete set",
    "description": "<p>Delete a user set</p>",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
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
    "filename": "Jiezi/accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsDelete_set"
  },
  {
    "type": "POST",
    "url": "/accounts/get_available_sets/",
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
    "filename": "Jiezi/accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsGet_available_sets"
  },
  {
    "type": "POST",
    "url": "/accounts/rename_set/",
    "title": "Rename set",
    "description": "<p>Rename a user set</p>",
    "group": "accounts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
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
    "filename": "Jiezi/accounts/views.py",
    "groupTitle": "accounts",
    "name": "PostAccountsRename_set"
  },
  {
    "type": "POST",
    "url": "/search/",
    "title": "Search",
    "description": "<p>search characters using ONE given keyword, it will be search against pinyin (without accent), chinese, 3 definitions</p>",
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
            "description": "<p>list of serialized Character objects</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "Jiezi/learning/views.py",
    "groupTitle": "general",
    "name": "PostSearch"
  },
  {
    "type": "POST",
    "url": "/learning/start_learning/",
    "title": "Start Learning",
    "description": "<p>Start Learning</p>",
    "success": {
      "examples": [
        {
          "title": "learning/review.html",
          "content": "context dictionary:\n'choices': a list of 4 strings\n'question': string of the question\n\nDisplay the question and choices with no next button\nAfter the user selects an answer, ajax POST to the same url with following args:\n    'user_answer': integer with range [0, 4), representing user's answer\nThe server responds with 'correct_answer', which is in the same range,\n    display the result, provide next button, and when the user clicks next, \n    submit GET request with no args\nrefer to old master review page for how to do specific things\n    https://github.com/chenyx512/jiezi/blob/old-master/jiezi/templates/learning/review_interface.html",
          "type": "json"
        },
        {
          "title": "learning/display_character.html:",
          "content": "There shouldn't be any ajax in this\nIn context dictionary, if 'is_next', provide an next button that submits\n    GET form to original url, otherwise keep the next button the same as before",
          "type": "json"
        }
      ]
    },
    "group": "learning",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "minutes_to_learn",
            "description": "<p>how many minutes to learn</p>"
          },
          {
            "group": "Parameter",
            "type": "int[]",
            "optional": false,
            "field": "uc_tags_filter",
            "defaultValue": "None",
            "description": "<p>(optional, None means everything) the ids of UserCharacterTags to INCLUDE</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "Jiezi/learning/views.py",
    "groupTitle": "learning",
    "name": "PostLearningStart_learning"
  }
] });

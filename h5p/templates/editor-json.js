Drupal Javascript to init the editor
Comparable to h5peditor-init.js we stole from somewhere. Probably needs
to be Django aware?

var H5PEditor = H5PEditor || {};
var ns = H5PEditor;
(function($) {
  ns.init = function () {
    var h5peditor;
    var $upload = $('input[name="files[h5p]"]').parents('.form-item');
    var $editor = $('.h5p-editor');
    var $create = $('#edit-h5p-editor').hide();
    var $type = $('input[name="h5p_type"]');
    var $params = $('input[name="json_content"]');
    var $library = $('input[name="h5p_library"]');
    var library = $library.val();

    ns.$ = H5P.jQuery;
    ns.basePath = Drupal.settings.basePath +  Drupal.settings.h5peditor.modulePath + '/h5peditor/';
    ns.contentId = Drupal.settings.h5peditor.nodeVersionId;
    ns.fileIcon = Drupal.settings.h5peditor.fileIcon;
    ns.ajaxPath = Drupal.settings.h5peditor.ajaxPath;
    ns.filesPath = Drupal.settings.h5peditor.filesPath;
    ns.relativeUrl = Drupal.settings.h5peditor.relativeUrl;
    ns.contentRelUrl = Drupal.settings.h5peditor.contentRelUrl;
    ns.editorRelUrl = Drupal.settings.h5peditor.editorRelUrl;

    // Semantics describing what copyright information can be stored for media.
    ns.copyrightSemantics = Drupal.settings.h5peditor.copyrightSemantics;

    // Required styles and scripts for the editor
    ns.assets = Drupal.settings.h5peditor.assets;

    // Required for assets
    ns.baseUrl = Drupal.settings.basePath;

    $type.change(function () {
      if ($type.filter(':checked').val() === 'upload') {
        $create.hide();
        $upload.show();
      }
      else {
        $upload.hide();
        if (h5peditor === undefined) {
          h5peditor = new ns.Editor(library, $params.val(), $editor[0]);
        }
        $create.show();
      }
    }).change();

    $('#h5p-content-node-form').submit(function () {
      if (h5peditor !== undefined) {
        var params = h5peditor.getParams();

        if (params === false) {
          // return false;
          /*
           * TODO: Give good feedback when validation fails. Currently it seems save and delete buttons
           * aren't working, but the user doesn't get any indication of why they aren't working.
           */
        }

        if (params !== undefined) {
          $library.val(h5peditor.getLibrary());
          $params.val(JSON.stringify(params));
        }
      }
    });
  };

  ns.getAjaxUrl = function (action, parameters) {
    var url = Drupal.settings.h5peditor.ajaxPath + action;

    if (parameters !== undefined) {
      for (var key in parameters) {
        url += '/' + parameters[key];
      }
    }

    return url;
  };

  $(document).ready(ns.init);
})(H5P.jQuery);
;

jQuery.extend(Drupal.settings, {"basePath":"\/","pathPrefix":"","ajaxPageState":{"theme":"professional_themec","theme_token":"lMhNFW9WN6eTzrvBOZeKlWTnwQxxU2p2DlbCNjp1QDA","js":{"sites\/all\/modules\/syntaxhighlighter\/syntaxhighlighter.min.js":1,"misc\/jquery.js":1,"misc\/jquery.once.js":1,"misc\/drupal.js":1,"misc\/vertical-tabs.js":1,"misc\/form.js":1,"sites\/all\/modules\/comment_notify\/comment_notify.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shCore.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shBrushCss.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shBrushJScript.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shBrushPhp.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shBrushSass.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shBrushSql.js":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/scripts\/shBrushXml.js":1,"sites\/all\/modules\/codefilter\/codefilter.js":1,"sites\/all\/modules\/h5p_org\/scripts\/h5p_org.js":1,"sites\/all\/modules\/h5p\/library\/js\/jquery.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-event-dispatcher.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-x-api-event.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-x-api.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-content-type.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-confirmation-dialog.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-action-bar.js":1,"sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-editor.js":1,"sites\/all\/modules\/h5p\/modules\/h5peditor\/scripts\/application.js":1,"sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/language\/en.js":1,"misc\/collapse.js":1,"sites\/all\/modules\/h5p\/library\/js\/h5p-display-options.js":1,"0":1,"sites\/all\/themes\/professional_themec\/js\/custom.js":1},"css":{"modules\/system\/system.base.css":1,"modules\/system\/system.menus.css":1,"modules\/system\/system.messages.css":1,"modules\/system\/system.theme.css":1,"misc\/vertical-tabs.css":1,"sites\/all\/modules\/comment_notify\/comment_notify.css":1,"sites\/all\/modules\/codefilter\/codefilter.css":1,"modules\/comment\/comment.css":1,"modules\/field\/theme\/field.css":1,"sites\/all\/modules\/logintoboggan\/logintoboggan.css":1,"modules\/node\/node.css":1,"modules\/user\/user.css":1,"modules\/forum\/forum.css":1,"sites\/all\/modules\/views\/css\/views.css":1,"sites\/all\/modules\/ctools\/css\/ctools.css":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/styles\/shCore.css":1,"sites\/all\/libraries\/syntaxhighlighter_3.0.83\/styles\/shThemeRDark.css":1,"sites\/all\/modules\/h5p_org\/styles\/h5p_org.css":1,"sites\/all\/modules\/location\/location.css":1,"sites\/all\/modules\/h5p\/library\/styles\/h5p.css":1,"sites\/all\/modules\/h5p\/library\/styles\/h5p-confirmation-dialog.css":1,"sites\/all\/modules\/h5p\/library\/styles\/h5p-core-button.css":1,"sites\/all\/modules\/feedback_simple\/feedback_simple.css":1,"sites\/all\/themes\/professional_themec\/css\/style.css":1,"sites\/all\/themes\/professional_themec\/css\/font-awesome.min.css":1}},"h5peditor":{"assets":{"css":["\/sites\/all\/modules\/h5p_org\/styles\/h5p_org.css?okcd3w","\/sites\/all\/modules\/h5p\/library\/styles\/h5p.css?okcd3w","\/sites\/all\/modules\/h5p\/library\/styles\/h5p-confirmation-dialog.css?okcd3w","\/sites\/all\/modules\/h5p\/library\/styles\/h5p-core-button.css?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/libs\/darkroom.css?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/styles\/css\/application.css?okcd3w"],"js":["\/sites\/all\/modules\/h5p\/library\/js\/jquery.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p-event-dispatcher.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p-x-api-event.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p-x-api.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p-content-type.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p-confirmation-dialog.js?okcd3w","\/sites\/all\/modules\/h5p\/library\/js\/h5p-action-bar.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-semantic-structure.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-library-selector.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-form.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-text.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-html.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-number.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-textarea.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-file-uploader.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-file.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-image.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-image-popup.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-av.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-group.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-boolean.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-list.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-list-editor.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-library.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-library-list-cache.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-select.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-dimensions.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-coordinates.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/scripts\/h5peditor-none.js?okcd3w","\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/ckeditor\/ckeditor.js?okcd3w"]},"filesPath":"\/sites\/default\/files\/h5peditor","fileIcon":{"path":"\/sites\/all\/modules\/h5p\/modules\/h5peditor\/h5peditor\/images\/binary-file.png","width":50,"height":50},"ajaxPath":"\/h5peditor\/aac6e1fe9af3b\/0\/","modulePath":"sites\/all\/modules\/h5p\/modules\/h5peditor","libraryPath":"sites\/default\/files\/h5p\/libraries\/","copyrightSemantics":{"name":"copyright","type":"group","label":"Copyright information","fields":[{"name":"title","type":"text","label":"Title","placeholder":"La Gioconda","optional":true},{"name":"author","type":"text","label":"Author","placeholder":"Leonardo da Vinci","optional":true},{"name":"year","type":"text","label":"Year(s)","placeholder":"1503 - 1517","optional":true},{"name":"source","type":"text","label":"Source","placeholder":"http:\/\/en.wikipedia.org\/wiki\/Mona_Lisa","optional":true,"regexp":{"pattern":"^http[s]?:\/\/.+","modifiers":"i"}},{"name":"license","type":"select","label":"License","default":"U","options":[{"value":"U","label":"Undisclosed"},{"value":"CC BY","label":"Attribution 4.0"},{"value":"CC BY-SA","label":"Attribution-ShareAlike 4.0"},{"value":"CC BY-ND","label":"Attribution-NoDerivs 4.0"},{"value":"CC BY-NC","label":"Attribution-NonCommercial 4.0"},{"value":"CC BY-NC-SA","label":"Attribution-NonCommercial-ShareAlike 4.0"},{"value":"CC BY-NC-ND","label":"Attribution-NonCommercial-NoDerivs 4.0"},{"value":"GNU GPL","label":"General Public License v3"},{"value":"PD","label":"Public Domain"},{"value":"ODC PDDL","label":"Public Domain Dedication and Licence"},{"value":"CC PDM","label":"Public Domain Mark"},{"value":"C","label":"Copyright"}]}]},"contentRelUrl":"..\/h5p\/content\/","editorRelUrl":"..\/..\/..\/h5peditor\/"},"urlIsAjaxTrusted":{"\/node\/add\/h5p-content":true}});

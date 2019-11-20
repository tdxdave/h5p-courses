var H5PEditor = H5PEditor || {};
var ns = H5PEditor;

/**
 * Creates a boolean field for the editor.
 *
 * @param {mixed} parent
 * @param {object} field
 * @param {mixed} params
 * @param {function} setValue
 * @returns {ns.Boolean}
 */
ns.Boolean = function (parent, field, params, setValue) {
  if (params === undefined) {
    this.value = false;
    setValue(field, this.value);
  }
  else {
    this.value = params;
  }

  this.field = field;
  this.setValue = setValue;
};

/**
 * Create HTML for the boolean field.
 */
ns.Boolean.prototype.createHtml = function () {
  var checked = (this.value !== undefined && this.value) ? ' checked' : '';
  var content = '<input type="checkbox"' + checked + ' />';

  return ns.createFieldMarkup(this.field, content);
};

/**
 * "Validate" the current boolean field.
 */
ns.Boolean.prototype.validate = function () {
  return true;
};

/**
 * Append the boolean field to the given wrapper.
 *
 * @param {jQuery} $wrapper
 * @returns {undefined}
 */
ns.Boolean.prototype.appendTo = function ($wrapper) {
  var that = this;

  this.$item = ns.$(this.createHtml()).appendTo($wrapper);
  this.$input = this.$item.find('input');
  this.$errors = this.$item.find('.h5p-errors');

  this.$input.change(function () {
    // Validate
    that.value = that.$input.is(':checked');
    that.setValue(that.field, that.value);
  });
};

/**
 * Remove this item.
 */
ns.Boolean.prototype.remove = function () {
  this.$item.remove();
};

// Tell the editor what widget we are.
ns.widgets['boolean'] = ns.Boolean;

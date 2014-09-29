FacetedEdit.OrdenarWidget = function(wid, context){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.ordenacao = jQuery('#ordenacao');
  this.select = jQuery('#' + this.wid);

  var value = this.select.val();
  this.selected = jQuery('option[value=' + value + ']', this.widget);

  // Handle select change
  var js_widget = this;

  this.ordenacao.change(function(evt){
    js_widget.set_default(this);
  });

};

FacetedEdit.OrdenarWidget.prototype = {
  set_default: function(element){
    var value = this.ordenacao.val();
    switch(value) {
      case 'effective':
          Faceted.Query.reversed = [];
          values = 'effective';
          break;
      case 'effective_reverse':
          values = 'effective';
          Faceted.Query.reversed = 'on';
          break;
      case 'sortable_title':
          values = 'sortable_title';
          Faceted.Query.reversed = [];
          break;
      case 'sortable_title_reverse':
          values = 'sortable_title';
          Faceted.Query.reversed = 'on';
          break;
      default:
          values = 'effective';
          Faceted.Query.reversed = [];
          break;
    }

    this.selected = jQuery('option[value=' + values + ']', this.widget);
    Faceted.Query[this.wid] = [values];

    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query[this.wid + '_default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeOrdenarWidget = function(){
  jQuery('div.faceted-ordenar-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.OrdenarWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeOrdenarWidget);
});

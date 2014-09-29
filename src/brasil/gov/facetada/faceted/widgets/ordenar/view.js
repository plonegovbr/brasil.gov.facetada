/* Ordenar Widget
*/
Faceted.OrdenarWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + this.wid + '_widget');
  this.widget.show();
  this.ordenacao = jQuery('#ordenacao');

  var error = jQuery('.faceted-widget:has(div.faceted-ordenar-errors)');
  if(error.length){
    error.remove();
    jQuery(Faceted.Events).trigger(Faceted.Events.REDRAW);
    return;
  }

  // Handle select change
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  var js_widget = this;
  this.ordenacao.change(function(evt){
    js_widget.ordenacao_change(this, evt);
  });

  // Default value
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
  Faceted.Query[this.wid] = [values];

  // Bind Events
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(){
    js_widget.reset();
  });
};

Faceted.OrdenarWidget.prototype = {
  ordenacao_change: function(element, evt){
    this.do_query(element);
  },

  do_query: function(element){
    value = jQuery(element).val();
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
    Faceted.Form.do_query(this.wid, values);
  },

  reset: function(){
    this.ordenacao.val("effective");
  },
};

Faceted.initializeOrdenarWidget = function(evt){
  jQuery('div.faceted-ordenar-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.OrdenarWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeOrdenarWidget);
});

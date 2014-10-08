var root = typeof exports !== "undefined" && exports !== null ? exports : this;

(function($) {
    // from collective.upload
    var config_upload_form  = function () {
        'use strict';
        //we have to check if the fileupload element existing
        if ($('#fileupload')[0] !== undefined) {
            var files_re = new RegExp('(\\.|\/)('+jupload.config['extensions']+')$', 'i');
            // Initialize the jQuery File Upload widget:
            $('#fileupload').fileupload({'sequentialUploads':true, 'singleFileUploads':true});

            // Enable iframe cross-domain access via redirect option:
            $('#fileupload').fileupload(
                'option',
                'redirect',
                window.location.href.replace(
                    /\/[^\/]*$/,
                    '/cors/result.html?%s'
                )
            );
            $('#fileupload').fileupload('option', {
                url: '',
                maxFileSize: jupload.config['max_file_size'],
                acceptFileTypes: files_re,
                process: [
                    {
                        action: 'load',
                        fileTypes: files_re,
                        maxFileSize: jupload.config['max_file_size']
                    },
                    {
                        action: 'resize',
                        maxWidth: jupload.config['resize_max_width'],
                        maxHeight: jupload.config['resize_max_height']
                    },
                    {
                        action: 'save'
                    }
                ],
                start_i18n: jupload.messages['START_MSG'],
                cancel_i18n: jupload.messages['CANCEL_MSG'],
                delete_i18n: jupload.messages['DELETE_MSG'],
                description_i18n: jupload.messages['DESCRIPTION_MSG'],
                error_i18n: jupload.messages['ERROR_MSG']
            });
            // Upload server status check for browsers with CORS support:
            if ($.support.cors) {
                $.ajax({
                    url: '',
                    type: 'HEAD'
                }).fail(function () {
                    $('<span class="alert alert-error"/>')
                        .text('Upload server currently unavailable - ' +
                                new Date())
                        .appendTo('#fileupload');
                });
            }

            // //in the latest version we have a method formData who actually is
            // // doing this...=)
            $('#fileupload').bind('fileuploadsubmit', function (e, data) {
                var inputs = data.context.find(':input');
                if (inputs.filter('[required][value=""]').first().focus().length) {
                    return false;
                }
                data.formData = inputs.serializeArray();
            });

            $(document).bind('drop', function (e) {
                var url = $(e.originalEvent.dataTransfer.getData('text/html')).filter('img').attr('src');
                if (url) {
                    $.getImageData({
                        url: url,
                        server:'http://localhost:8080/Plone/@@jsonimageserializer?callback=?',
                        success: function (img) {
                            var canvas = document.createElement('canvas');
                            canvas.width = img.width;
                            canvas.height = img.height;
                            if (canvas.getContext && canvas.toBlob) {
                                canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
                                canvas.toBlob(function (blob) {
                                    $('#fileupload').fileupload('add', {files: [blob]});
                                }, "image/jpeg");
                            }
                        },
                        error: function(xhr, text_status){
                            // Handle your error here
                        }
                    });
                }
                e.preventDefault();
            });
        }
    };
    // from collective.upload

    root.ImageSelectionDialog = function(callback) {
        var ImageSelectionDialog, _base;
        ImageSelectionDialog = (function() {
            function ImageSelectionDialog(callback) {
                this.callback      = callback;
                this.base_url      = $('head>link[rel=stylesheet][href*=portal_css]:first')[0].href.split('/portal_css')[0];
                var ws = window.location.href.split('/');
                ws[ws.length - 1] = 'folder_contents';
                this.actual_folder = ws.join('/');
                this.dialog_width  = 750;
                this.dialog_height = 425;
                this.selected      = null;
                this.create_dialog();
            }
            ImageSelectionDialog.prototype.fix_html = function(data) {
                var $retorno = data;
                // Traz só o conteúdo principal
                $retorno = $('#content-core', $retorno);

                // Adicionar localização
                var breadcrumb = this.actual_folder.slice(this.base_url.length, ('folder_contents'.length * -1)),
                    $span = $('<span>');
                $span.addClass('breadcrumb');
                $span.text('Voce está em: ' + breadcrumb);
                $('form[name=folderContentsForm]', $retorno).prepend($span);

                // Adicionar título
                var $span = $('<span>');
                $span.addClass('title');
                $span.text('Selecione uma imagem:');
                $('form[name=folderContentsForm]', $retorno).prepend($span);

                // Mover link para nivel acima para baixo
                $('#folderlisting-main-table', $retorno).prepend($('a.link-parent', $retorno));

                // Add preview
                $div = $('<div>');
                $div.addClass('preview');
                $align = $('<div>');
                $align.addClass('table-align');
                this.$preview = $('<img>');
                $align.append(this.$preview);
                $div.append($align);
                $('form[name=folderContentsForm]', $retorno).append($div);

                // Remover header
                $('#listing-table > thead', $retorno).remove();

                // Remover footer
                $('#listing-table > tfoot', $retorno).remove();

                // Remover botões desnecessários
                $('#folderlisting-main-table > input', $retorno).remove();

                // Remove colunas não usadas
                var i, _i, _len, _ref;
                _ref = [1, 2, 4, 5, 6].reverse();
                for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                    i = _ref[_i];
                    $('#listing-table tr > th:nth-child('+i+')', $retorno).remove();
                    $('#listing-table tr > td:nth-child('+i+')', $retorno).remove();
                }

                // Remove itens que não são pastas ou imagens
                $('#listing-table > tbody tr', $retorno).each(function() {
                    var $this = $(this);
                    if (!$('a.contenttype-folder, a.contenttype-image', $this).length) {
                        $this.remove();
                    }
                });

                // Override de regra com important
                this.$dialog
                    .parent()[0]
                    .style
                    .setProperty('width',
                                 this.dialog_width + 'px',
                                 'important');

                // Fix dialog position
                var page_width      = $(window).width(),
                    dialog_position = ((page_width        /
                                        2)                -
                                       (this.dialog_width /
                                        2));
                this.$dialog.parent().css('left', dialog_position);

                return $retorno;
            };
            ImageSelectionDialog.prototype.bind_events = function() {
                // from collective.upload main.js
                config_upload_form();

                // Recarrega pasta após upload
                $('#fileupload').bind('fileuploadstop', function() {
                    var isd = new root.ImageSelectionDialog();
                    isd.get_folder();
                });

                // Subir uma pasta
                $('.image-upload-dialog #folderlisting-main-table a.link-parent').on('click', function(e) {
                    e.preventDefault();
                    var isd = new root.ImageSelectionDialog(),
                        $a  = $(this);
                    isd.get_folder($a.attr('href'));
                });

                // Click em um item
                $('.image-upload-dialog #folderlisting-main-table td').on('click', function(e) {
                    e.preventDefault();
                    var isd = new root.ImageSelectionDialog(),
                        $tr = $(this).parent(),
                        $a  = $('a', $tr);
                    if ($a.hasClass('contenttype-folder')) {
                        isd.get_folder($a.attr('href'));
                    } else if ($a.hasClass('contenttype-image')) {
                        $('.image-upload-dialog #folderlisting-main-table tr').removeClass('selected');
                        $tr.addClass('selected');
                        var re     = new RegExp('(.*)/view$'),
                            imgurl = $a.attr('href').match(re)[1];
                        $.ajax({
                            url: imgurl + '/@@scaleimage',
                            type: 'GET',
                            dataType: 'json',
                            data: {
                                scale: 'mini',
                            },
                        }).done((function(that) {
                            return function(data) {
                                that.selected = data['path']
                                that.$preview.attr('src', data['url'])
                            }
                        })(isd));
                    }
                });
            };
            ImageSelectionDialog.prototype.get_folder = function(folder) {
                if (!folder) {
                    folder = this.actual_folder;
                }
                var sfolder = folder.split('/');
                if (sfolder[sfolder.length -1] !== 'folder_contents') {
                    folder += '/folder_contents';
                }
                this.actual_folder = folder;
                $.ajax({
                    url: folder,
                    type: 'GET',
                    data: {
                        'show_all': true,
                    },
                }).done((function(that) {
                    return function(data) {
                        that.$dialog.html(that.fix_html(data));
                        that.bind_events();
                    };
                })(this));
            };
            ImageSelectionDialog.prototype.create_dialog = function() {
                (function(that) {
                    that.$dialog = $('.image-upload-dialog');
                    if (!that.$dialog.length) {
                        that.$dialog = $('<div>');
                        that.$dialog.addClass('image-upload-dialog');
                        $('#faceted-edit-widgets-ajax').append(that.$dialog);
                    }
                    that.$dialog.dialog({
                        width: that.dialog_width,
                        height: that.dialog_height,
                        title: 'Upload de imagens',
                        bgiframe: true,
                        modal: true,
                        autoOpen: false,
                        buttons: {
                            'Selecionar': that.select,
                            'Fechar': that.close,
                        },
                        close: that.close
                    });
                    that.get_folder();
                    that.$dialog.dialog('open');
                })(this);
            };
            ImageSelectionDialog.prototype.select = function() {
                var isd = new root.ImageSelectionDialog();
                isd.callback(isd.selected);
                isd.close();
            };
            ImageSelectionDialog.prototype.close = function() {
                var isd = new root.ImageSelectionDialog();
                isd.$dialog.dialog('close');
                isd.$dialog.remove();
                root.ImageSelectionDialog.instance = null;
            };
            return ImageSelectionDialog;
        })();

        if ((_base = root.ImageSelectionDialog).instance == null) {
            _base.instance = new ImageSelectionDialog(callback);
        }
        return root.ImageSelectionDialog.instance;
    };

    var updateThumb = function(imgpath) {
        var base_url = $('head>link[rel=stylesheet][href*=portal_css]:first')[0].href.split('/portal_css')[0];
        $.ajax({
            url: base_url + '/@@scaleimage',
            type: 'GET',
            dataType: 'json',
            data: {
                path: imgpath,
                scale: 'thumb',
            },
        }).done(function(data) {
            $('.isu_imagem').attr('src', data['url'])
        });
    };

    $('.faceted-banner-widget .ui-icon-pencil').live('click', function() {
        setTimeout(function() {
            var imgpath = $('.upload_imagem').val();
            if (imgpath) {
                updateThumb(imgpath);
            }
        }, 300);
    });

    $('.isu_selecionar_imagem').live('click', function(e) {
        e.preventDefault();
        new root.ImageSelectionDialog(function(selected) {
            $('.upload_imagem').val(selected);
            updateThumb(selected);
        });
    });
})(jQuery);
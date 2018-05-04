/**
 * Created by kubixpc on 17.02.2017.
 */
$(function() {
    // Multiple images preview in browser
    var imagesPreview = function (input, placeToInsertImagePreview) {

        if (input.files) {
            var filesAmount = input.files.length;

            for (i = 0; i < filesAmount; i++) {
                var reader = new FileReader();

                reader.onload = function (event) {
                    //$($.parseHTML('<img>')).attr('src', event.target.result).appendTo(placeToInsertImagePreview);
                    var image = '<a href="'+event.target.result+'" class="">'+
                    '<div class="img">'+
                    '<img src="'+event.target.result+'" alt="">'+
                    '</div>'+
                    '<i class="fa fa-search-plus icon"></i>'+
                    '</a>';
                    $(placeToInsertImagePreview).append(image);
                };

                reader.readAsDataURL(input.files[i]);
            }
        }

    };

    $('#id_images').on('change', function () {
        imagesPreview(this, 'div.gallery');
    });
});
$(document).ready(function() {
    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
            
            // Upload image to server
            var formData = new FormData();
            formData.append('fileToUpload', input.files[0]); // Thay đổi tên trường thành 'fileToUpload'

            $.ajax({
                url: '/update',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    console.log('Image uploaded successfully.');
                    // Thêm phần xử lý sau khi hình ảnh tải lên thành công (nếu cần)
                },
                error: function(xhr, status, error) {
                    console.log('Image upload failed:', error);
                    // Thêm phần xử lý khi tải lên hình ảnh thất bại (nếu cần)
                }
            });
        }
    }

    $(".file-upload").on('change', function(){
        readURL(this);
    });

    $(".upload-button").on('click', function() {
        $(".file-upload").click();
    });
});
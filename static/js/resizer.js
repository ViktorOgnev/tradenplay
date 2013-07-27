window.onload = countImgs('60px', 'auto', 'resizable_image'); 
/* function resizeImages(){
    var resizable_images = document.getElementsByClassName('resizable_image');
    
    for (image in resizable_images) {
        image.style.width='60px';
        image.style.height='auto';
    }    
}; */


function countImgs(maxHeight, maxWidth, class_name)
{
    var img = document.images;
    
    for (var i = 0; i < img.length; i++) {
        if (img[i].className == class_name){
            if (img[i].height > maxHeight){
                img[i].height = maxHeight;
                document.log(i)
            }
            if (img[i].style.width > maxWidth) {
                img[i].style.width = maxWidth;
                document.log(i*i)
            }
        }
    }
    
}

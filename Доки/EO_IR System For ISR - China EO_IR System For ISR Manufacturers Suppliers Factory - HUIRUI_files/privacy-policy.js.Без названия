/* Privacy statement - Privacy Policy */
var $wmkcprivacydata;
var wmkcprivacy = localStorage.getItem('wmkcprivacy');
if (wmkcprivacy == undefined || wmkcprivacy == 'false') {
  localStorage.setItem('wmkcprivacy', 'false');
  wmkcprivacyDialog();
}

function wmkcprivacyDialog() {
  $('body').append('<div id="wmkcprivacy"></div>')
  $('#wmkcprivacy').html("<style>#wmkcprivacy{position:fixed;bottom:calc(10px + constant(safe-area-inset-bottom));bottom:calc(10px + env(safe-area-inset-bottom));right:10px;width:360px;z-index:999999}#wmkcprivacy.left{left:10px;right:auto}#wmkcprivacy.right{left:auto;right:10px}#wmkcprivacy *{padding:0;margin:0;box-sizing:border-box;border:none;outline:0;font-size:16px;color:#000;line-height:1;font-weight:400;text-decoration:none}#wmkcprivacy .wmkcprivacy-wrap{display:block;width:100%;height:100%;background:#fff;border-radius:10px;padding:15px;transition:all .1s linear;box-shadow:1px 2px 10px rgba(0,0,0,.2)}#wmkcprivacy .wmkcprivacy-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}#wmkcprivacy .wmkcprivacy-close{width:25px;height:25px;background:#eee;border-radius:50%;cursor:pointer;position:relative;transition:all .1s linear}#wmkcprivacy .wmkcprivacy-close::after,#wmkcprivacy .wmkcprivacy-close::before{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(45deg);width:13px;height:2px;background:#999;transition:all .1s linear}#wmkcprivacy .wmkcprivacy-close::after{transform:translate(-50%,-50%) rotate(-45deg)}#wmkcprivacy .wmkcprivacy-close:hover{background:var(--color,#ddd)}#wmkcprivacy .wmkcprivacy-close:hover::after,#wmkcprivacy .wmkcprivacy-close:hover::before{background:#fff}#wmkcprivacy .wmkcprivacy-title{font-size:18px;font-weight:600;color:#333;border-radius:5px}#wmkcprivacy .wmkcprivacy-content,#wmkcprivacy .wmkcprivacy-content *{font-size:14px;line-height:22px;color:#555}#wmkcprivacy .wmkcprivacy-content .wmkcprivacy-lmore{text-decoration:underline;text-transform:lowercase;padding-left:3px}#wmkcprivacy .wmkcprivacy-content .wmkcprivacy-lmore:hover{color:var(--color)}#wmkcprivacy .wmkcprivacy-footer{display:flex;align-items:center;justify-content:space-between;margin-top:15px}#wmkcprivacy .wmkcprivacy-footer .wmkcprivacy-reject{color:#666;font-size:12px;transition:all .1s linear;text-transform:lowercase;padding-right:5px;line-height:1.6}#wmkcprivacy .wmkcprivacy-footer .wmkcprivacy-reject em{color:#666;font-size:14px;text-transform:capitalize;cursor:pointer;text-decoration:underline;font-style:inherit}#wmkcprivacy .wmkcprivacy-footer .wmkcprivacy-reject em:hover{color:var(--color,#555)}#wmkcprivacy .wmkcprivacy-footer a:hover{color:#333}#wmkcprivacy .wmkcprivacy-btn{background:var(--color,#2189ff);display:block;padding:12px 25px;color:#fff;cursor:pointer;border-radius:30px;transition:all .1s linear;font-size:14px}#wmkcprivacy .wmkcprivacy-btn:hover{opacity:.9}.wmkcprivacy-animate{animation:wmkcprivacyfade .5s forwards}@keyframes wmkcprivacyfade{0%{opacity:1;right:40px}100%{opacity:0;right:-100px;visibility:hidden}}@media (max-width:768px){#wmkcprivacy{width:100%;max-width:100%;left:0!important;right:auto!important;bottom:calc(onstant(safe-area-inset-bottom));bottom:calc(env(safe-area-inset-bottom));margin:0}#wmkcprivacy .wmkcprivacy-wrap{border-radius:0;border-top:1px solid #f3f3f3}@keyframes wmkcprivacyfade{0%{opacity:1;left:0}100%{opacity:0;left:-100px;visibility:hidden}}}</style>")

  $.ajax({
    url: '/OutOpen/GetPrivacyReturn',
    type: 'get',
    dataType: 'json',
    success: function (data) {
      $wmkcprivacydata = data;
      $('#wmkcprivacy').append(`<div class="wmkcprivacy-wrap"><div class="wmkcprivacy-header"><div class="wmkcprivacy-title">${$wmkcprivacydata.title || 'Cookie Usage'}</div><span class="wmkcprivacy-close" title="Close"></span></div><div class="wmkcprivacy-content">${$wmkcprivacydata.content || 'In order to provide you with a better browsing experience, this website will use cookies. By clicking "Accept" or continuing to browse this website, you agree to our use of cookies.'}&nbsp;<a href="/privacy-policy" rel="nofollow" class="wmkcprivacy-lmore">${$wmkcprivacydata.btn1}</a></div><div class="wmkcprivacy-footer"><span class="wmkcprivacy-reject"><em title="Reject - click here to reject the cookies">${$wmkcprivacydata.btn3}</em> - ${$wmkcprivacydata.btn4}</span> <button class="wmkcprivacy-btn" onclick="try{gtag();}catch(error){}try{ allConsentGranted();}catch(error){}">${$wmkcprivacydata.btn2}</button></div></div>`);
      if ($wmkcprivacydata.Position == 1) {
        $('#wmkcprivacy').addClass('left');
      } else {
        $('#wmkcprivacy').addClass('right');
      }
      Operational();
    },
    error: function () {
      $('#wmkcprivacy').append('<div class="wmkcprivacy-wrap right"><div class="wmkcprivacy-header"><div class="wmkcprivacy-title">Cookie Usage.</div><span class="wmkcprivacy-close" title="Close"></span></div><div class="wmkcprivacy-content">In order to provide you with a better browsing experience, this website will use cookies. By clicking "Accept" or continuing to browse this website, you agree to our use of cookies. &nbsp;<a href="/privacy-policy" class="wmkcprivacy-lmore">Learn more</a></div><div class="wmkcprivacy-footer"><span class="wmkcprivacy-reject"><em title="Reject - click here to reject the cookies">Reject</em> - click here to reject the cookies</span> <button class="wmkcprivacy-btn" onclick="try{gtag();}catch(error){}try{ allConsentGranted();}catch(error){}">Accept</button></div></div>');
      Operational();
    }
  });
}

function Operational() {
  $('.wmkcprivacy-close').click(function () {
    $('#wmkcprivacy').remove();
  })
  $('.wmkcprivacy-btn, .wmkcprivacy-reject em').click(function () {
    $('#wmkcprivacy').addClass('wmkcprivacy-animate');
    localStorage.setItem('wmkcprivacy', 'true');
    setTimeout(function () {
      $('#wmkcprivacy').remove();
    }, 1000)
  })
}
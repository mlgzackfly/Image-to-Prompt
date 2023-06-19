var dropbox = document.getElementById("dropbox");
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);

function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}

function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  var dt = e.dataTransfer;
  var files = dt.files;

  var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

   // 建立 FormData 物件並加入拖曳的圖片
  var formData = new FormData();
  for (var i = 0; i < files.length; i++) {
    formData.append("upload", files[i]);
  }
  formData.append("csrfmiddlewaretoken",csrfToken)

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "app", true);
  xhr.setRequestHeader("X-CSRFToken", csrfToken); // 添加 CSRF Token 到標頭

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
         // 請求成功，回應正確
        var response = JSON.parse(xhr.responseText);
        // 在此處理後端回應的資料
        updatePage(response);
      } else {
        // 請求失敗或回應錯誤
        console.error("請求失敗");
      }
    }
  };

  xhr.send(formData);


}
function updatePage(data) {
  // 根據後端回應的資料更新頁面
  var resultElement = document.getElementsByClassName("ts-badge");
  // 在這裡操作 resultElement，例如將資料插入到DOM元素中
  resultElement.innerHTML = data.tags;
}

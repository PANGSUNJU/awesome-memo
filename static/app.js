async function editMemo(event) {
  const id = event.target.dataset.id;
  const editInput = prompt("수정할 값을 입력하세요");
  // fetch 파람값을 보내거나 받을 때 백틱(`)으로 감싸주어야한다.
  const res = await fetch(`memos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      title: editInput,
      createAt:'',
    }),
  });
  readMemo();
}

async function deleteMemo(event) {
  const id = event.target.dataset.id;
  const res = await fetch(`memos/${id}`, {
    method: "DELETE",
  });

  readMemo();
}

function displayMemo(memo) {
  const ul = document.querySelector("#memo-ul");
  const li = document.createElement("li");
  li.innerText = `[id:${memo.id}] ${memo.title} ${memo.createAt}`;

  const editBtn = document.createElement("button");
  editBtn.innerText = "수정하기";
  editBtn.addEventListener("click", editMemo);
  editBtn.dataset.id = memo.id;

  const delBtn = document.createElement("button");
  delBtn.innerText = "삭제";
  delBtn.dataset.id = memo.id;
  delBtn.addEventListener("click", deleteMemo);

  li.appendChild(editBtn);
  li.appendChild(delBtn);
  ul.appendChild(li);
}

async function readMemo() {
  const res = await fetch("/memos");
  const jsonRes = await res.json();
  const ul = document.querySelector("#memo-ul");
  ul.innerHTML = "";
  //jsonRes[{id:123,content:'블라블라'}]
  jsonRes.forEach(displayMemo);
}

async function createMemo(value) {
  let createTime = new Date();
  let mouth = createTime.getMonth();
  let day = createTime.getDay();
  let h = createTime.getHours();
  let m = createTime.getMinutes();
  let s = createTime.getSeconds();
  
  let CreateAt = ` ${mouth}/${day} ${h}:${m}:${s}`
  let id = `${createTime.getTime()}`
  const res = await fetch("/memos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      title: value,
      createAt: CreateAt,
    }),
  });
  readMemo();
}

function handleSubmit(event) {
  event.preventDefault();
  const input = document.querySelector("#memo-input");
  createMemo(input.value);
  input.value = "";
}
const form = document.querySelector("#memo-form");
form.addEventListener("submit", handleSubmit);

readMemo();

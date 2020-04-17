var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

var apiAllReply = function(callback) {
    var method = 'GET'
    var path = '/reply/api/all?topic_id={{ tid }}'
    ajax(method, path, '', callback)
}

var apiAddReply = function(form, callback) {
    var method = 'POST'
    var path = '/reply/api/add'
    ajax(method, path, form, callback)
}

var template = function(r) {
    var m = `
        <div class="cell uid-${r.user_id}">
            <span>${r.content}</span>
        </div>
    `
    return m
}

var insertReply = function(r) {
    var m = template(r)
    var list = e('.replies_list')
    list.insertAdjacentHTML('beforeend', m)
}

var loadReplies = function() {
    apiAllReply(function(response) {
        var forms = JSON.parse(response)
        for (var i = 0; i < forms.length; i++) {
            var r = forms[0]
            insertReply(r)
        }
    })
}


var bindBtnEvent = function() {
    var btn = e('.btn-reply')
    btn.addEventListener('click', function() {
        var content = e('.content')
        var form = {
            'topic_id': parseInt(content.dataset.tid),
            'user_id': parseInt(content.dataset.uid),
            'content': content.value,
        }
        apiAddReply(form, function(response) {
            var r = JSON.parse(response)
            insertReply(r)
            content.value = ''
        })
    })
}

var bindEvents = function() {
    bindBtnEvent()
}

log('aaaaaa')
var __main = function() {
    log('sdfgsdf')
    bindEvents()
    log('111')

    loadReplies()
    log('222')

}
log('bbb')
__main()
log('ccc')
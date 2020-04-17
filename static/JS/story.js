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

var apiDpcqNext = function(callback) {
    var method = 'GET'
    var path = '/story/api/dpcq/next'
    ajax(method, path, '', callback)
}

var apiDpcqLast = function(callback) {
    var method = 'GET'
    var path = '/story/api/dpcq/last'
    ajax(method, path, '', callback)
}

var apiDldlNext = function(callback) {
    var method = 'GET'
    var path = '/story/api/dldl/next'
    ajax(method, path, '', callback)
}

var apiDldlLast = function(callback) {
    var method = 'GET'
    var path = '/story/api/dldl/last'
    ajax(method, path, '', callback)
}

var nextButtonEvent = function () {
    var nextButton = e('.button.next')
    nextButton.addEventListener('click', function() {
        var jsTitle = e('.js-title')
        var jsContent = e('.js-content')
        var storyTag = e('.tag_story')
        if(storyTag.value === 'dpcq') {
            apiDpcqNext(function(response) {
                var form = JSON.parse(response)
                jsTitle.innerHTML = form.title
                jsContent.innerHTML = form.content
                $('html, body').animate({scrollTop:700}, 500)
            })
        }else {
            apiDldlNext(function(response) {
                var form = JSON.parse(response)
                jsTitle.innerHTML = form.title
                jsContent.innerHTML = form.content
                $('html, body').animate({scrollTop:700}, 500)
            })
        }
    })
}

var lastButtonEvent = function () {
    var lastButton = e('.button.last')
    lastButton.addEventListener('click', function() {
        var jsTitle = e('.js-title')
        var jsContent = e('.js-content')
        var storyTag = e('.tag_story')
        if(storyTag.value === 'dpcq') {
            apiDpcqLast(function(response) {
                var form = JSON.parse(response)
                jsTitle.innerHTML = form.title
                jsContent.innerHTML = form.content
                $('html, body').animate({scrollTop:700}, 500)
            })
        }else {
            apiDldlLast(function(response) {
                var form = JSON.parse(response)
                jsTitle.innerHTML = form.title
                jsContent.innerHTML = form.content
                $('html, body').animate({scrollTop:700}, 500)
            })
        }
    })
}

var bindEvents = function () {
    nextButtonEvent()
    lastButtonEvent()
}

var __main = function () {
    bindEvents()
}

__main()

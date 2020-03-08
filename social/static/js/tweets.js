$(function() {
    // get top level container
    const $container = $('#tweet-feed');

    // retrieve CSRF token
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    const getTweetElement = function(tweet) {
        // create tweet
        const $tweet = $('<div />')
            .addClass('tweet')
            .append($('<div />')
                .addClass('user')
                .text(tweet.user.name)
            )
            .append($('<div />')
                .addClass('posted-at')
                .text(`, posted at ${tweet.created}`)
            )
            .append($('<div />')
                .addClass('content')
                .text(tweet.message)
            );

        // add controls if tweet is mine
        if (tweet.user.meter_number === window.USER.meterNumber) {

        }

        return $tweet
    };

    const loadFeed = function($feedContainer) {
        // set loading
        $feedContainer.append($('<div />').text('Loading...'));

        // load feed
        $.ajax({
            url: '/social/tweets/',
            method: 'GET',
            success: function({tweets}) {
                // unset loading
                $feedContainer.empty();

                // add tweets
                $.each(tweets, function(idx, tweet) {
                    // add to container
                    $feedContainer.append(getTweetElement(tweet));
                });
            }
        })
    };

    const postTweet = function($feedContainer) {
        const $btn = $container.find('button.post-tweet');

        // get input and ensure a message has been typed
        const $inp = $container.find('textarea');

        if (!$inp.val()) {
            return
        }

        // check if still enable
        // if yes, disable until post
        if ($btn.attr('disabled')) {
            return
        }

        $btn
            .attr('disabled', 'disabled')
            .text('Posting...');

        // get message & clear input
        const message = $inp.val();
        $inp.val('');

        // post to backend
        $.ajax({
            url: '/social/tweets/create/',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken,
                message: message
            },
            success: function({tweet}) {
                $feedContainer.prepend(
                    getTweetElement(tweet)
                );

                // remove disabled
                $btn
                    .removeAttr('disabled')
                    .text('Post');
            }
        });
    };

    // add form & feed
    const $feedContainer = $('<div />')
        .addClass('feed');

    const $formContainer = $('<div />')
        .addClass('form-post')
        .append($('<textarea />')
            .attr('placeholder', 'Post your thoughts here...')
            .on('keyup', function(e) {
                if (e.keyCode === 13){
                    postTweet($feedContainer);
                }
            })
        )
        .append($('<button />')
            .addClass('btn btn-primary post-button')
            .text('Post')
            .on('click', function() {
                postTweet($feedContainer);
            })
        );

    // add both to container
    $container
        .append($formContainer)
        .append($feedContainer);

    // load feed
    loadFeed($feedContainer);
});
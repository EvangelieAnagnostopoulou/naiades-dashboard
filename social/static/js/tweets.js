$(function() {
    const setupContainer = function($container, config) {
        config = config || {};

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
                    .text(`, ${window.MESSAGES.tweets.postedAt} ${tweet.created}`)
                )
                .append($('<div />')
                    .addClass('content')
                    .text(tweet.message)
                );

            return $tweet
        };

        const loadFeed = function($feedContainer) {
            // set loading
            $feedContainer.append($('<div />').text(`${window.MESSAGES.tweets.loading}...`));

            // load feed
            $.ajax({
                url: `/social/tweets/${config.schoolId ? `?school=${config.schoolId}` : ''}`,
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
                .text(`${window.MESSAGES.tweets.posting}...`);

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
                    // remove disabled
                    $btn
                        .removeAttr('disabled')
                        .text('Post');

                    // show message if pending for moderation
                    if (!tweet.is_accepted) {
                        return window.alert(window.MESSAGES.tweets.success);
                    }

                    $feedContainer.prepend(
                        getTweetElement(tweet)
                    );
                }
            });
        };

        // add form & feed
        const $feedContainer = $('<div />')
            .addClass('feed');

        const $formContainer = config.canPostTweet ? $('<div />')
            .addClass('form-post')
            .append($('<textarea />')
                .attr('placeholder', `${window.MESSAGES.tweets.postThoughtsHere}...`)
                .on('keyup', function(e) {
                    if (e.keyCode === 13){
                        postTweet($feedContainer);
                    }
                })
            )
            .append($('<button />')
                .addClass('btn btn-primary post-button')
                .text(window.MESSAGES.tweets.post)
                .on('click', function() {
                    postTweet($feedContainer);
                })
            ) : null;

        // add both to container
        $container
            .append($formContainer)
            .append($feedContainer);

        // load feed
        loadFeed($feedContainer);
    };

    // setup in top level container
    setupContainer($('#tweet-feed--all'), {
        canPostTweet: true
    });

    // setup for my school
    const $schoolFeed = $('#tweet-feed--school');
    setupContainer($schoolFeed, {
        canPostTweet: false,
        schoolId: $schoolFeed.data('schoolid')
    });
});
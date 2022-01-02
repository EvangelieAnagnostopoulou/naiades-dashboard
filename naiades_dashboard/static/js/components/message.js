const addMessage = function($container, data, messageId) {
    $container.append(
        $('<div />')
            .attr('id', messageId)
            .append($('<span />')
                .append($('<i />')
                    .addClass(`fa fa-comment`)
                )
                .append($('<span />')
                    .text(data[0])
                )
            )
    );
};


window.COMPONENT_CALLBACKS.message = function($container, metric, data) {
    addMessage($container, data, 'main-message')
};

window.COMPONENT_CALLBACKS.message_change = function($container, metric, data) {
    addMessage($container, data, 'message-change')
};

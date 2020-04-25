window.COMPONENT_CALLBACKS.message = function($container, metric, data) {
    $container.append(
        $('<div />')
            .attr('id', 'main-message')
            .append($('<span />')
                .append($('<i />')
                    .addClass(`fa fa-${data[0].type === "SUCCESS" ? "smile" : "frown"}-o`)
                )
                .append($('<span />')
                    .text(data[0].message)
                )
            )
    );
};
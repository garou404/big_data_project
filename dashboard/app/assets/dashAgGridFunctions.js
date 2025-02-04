var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};


dagcomponentfuncs.svgRenderer = function (props) {
    console.log(props)
    // if (!params.value) return "";
    // return `<img src="${params.value}" width="50" height="50" style="border: 1px solid #ddd;" />`;
    return React.createElement(
        'div',
        {
            style: {
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
            },
        },
        React.createElement(
            'img',
            {
                style: {width: '30px', height: 'auto'},
                src: props.value,

            },
        ))
}
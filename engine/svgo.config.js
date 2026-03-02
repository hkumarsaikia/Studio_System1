export default {
    plugins: [
        {
            name: 'preset-default',
        },
        'removeViewBox' // Moved out of preset-default since it's an independent plugin in SVGO v3+
    ],
};

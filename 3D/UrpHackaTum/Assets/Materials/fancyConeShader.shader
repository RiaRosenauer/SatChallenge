Shader "Custom/fancyConeShader"
{
    Properties
    {
        [MaterialToggle] _isToggled("accurate doppler", Float) = 0
        _dopplerThreshold("doppler threshold in kHz", Range(0.,2.5)) = 2.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        LOD 200

        CGPROGRAM
        // Physically based Standard lighting model, and enable shadows on all light types
        #pragma surface surf Standard fullforwardshadows

        // Use shader model 3.0 target, to get nicer looking lighting
        #pragma target 3.0
        
        struct Input
        {
            float2 uv_MainTex;
            float3 worldPos : TEXCOORD0;
        };


        half _Glossiness;
        half _Metallic; 
        bool _isToggled;
        float _dopplerThreshold;
        # define PI 3.1415926535
        # define RE 6.380
        # define G 6.67430e-11
        # define C 3e8
        # define M_earth 5.97e24
        # define E_ROT_RATE 2.*PI/24./60./60.
        fixed4 _Color;
        #define numberOfSats  256
        fixed4 _Points[numberOfSats];
        fixed4 _OrbitNormals[numberOfSats];

        // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
        // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
        // #pragma instancing_options assumeuniformscaling
        UNITY_INSTANCING_BUFFER_START(Props)
            // put more per-instance properties here
        UNITY_INSTANCING_BUFFER_END(Props)

        void surf (Input IN, inout SurfaceOutputStandard o)
        {
            //IN.worldPos
            fixed4 value = fixed4(0.,0.,0.,1.);
            for (int i = 0; i < numberOfSats; ++i) {
                fixed3 earth_to_sat_unit = normalize(_Points[i].xyz - IN.worldPos);

                float dotp = dot(normalize(IN.worldPos), earth_to_sat_unit);

                float r = length(_Points[i].xyz);

                float b_max = (90. + 10.) / 180. * PI;
                float b_min = (90 + 75.) / 180. * PI;

                float theta_max = -(asin(RE * sin(b_max) / r)+ b_max - PI);
                float theta_min = -(asin(RE * sin(b_min) / r) + b_min - PI);

                if(dotp < cos(theta_min) && dotp>cos(theta_max)){
                    value += fixed4(0., .2, 0., 0.);

                    // doppler effect
                    fixed3 v_earth = cross(fixed3(0., E_ROT_RATE,0.), IN.worldPos * 1e6);

                    float velocity = sqrt(M_earth * G / (r * 1e6));

                    fixed3 v_orbit = _OrbitNormals[i].xyz * velocity;
                    fixed3 v = v_orbit - v_earth;


                    float f_delta = 0.;
                    if (_isToggled>.5) {
                        //accurate vector based doppler shift
                        f_delta = 137e3 * dot(v, earth_to_sat_unit) / C;
                    }
                    else {
                        //the handwavy doppler equation from the presentation (1ppm per 1000km/h)
                        f_delta = 137e3 * length(v) * 3.6e-3 * 1e-6;
                    }
                    // add the worst case doppler shift (1ppm) of a plane flying in the opposing direction (1000km/h)
                    f_delta += sign(f_delta) * 137e3 * 1e-6; 

                    if (abs(f_delta) > _dopplerThreshold) {
                        if(f_delta>0.)
                            //positive doppler shift (blue)
                            value += fixed4(.2, -.2, 0., 0.);
                        else
                            //negative doppler shift (red)
                            value += fixed4(0., -.2, .2, 0.);
                    }
                }
            }
            o.Albedo = value.rgb;
            
        }
        ENDCG
    }
    FallBack "Diffuse"
}

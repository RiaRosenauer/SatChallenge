using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SatPosBinder : MonoBehaviour
{

    Material coneMaterial;
    private GameObject[] sats;
    private Vector4[] points = new Vector4[256];
    private Vector4[] motionNormals = new Vector4[256];

    // Start is called before the first frame update
    void OnValidate()
    {
#if UNITY_EDITOR
        updateShader();
#endif
    }

    private void Update()
    {
        updateShader();
    }

    void updateShader()
    {
        sats = GameObject.FindGameObjectsWithTag("Satellite");
        coneMaterial = GetComponent<MeshRenderer>().sharedMaterial;

        for (int i = motionNormals.Length - 1; i >= sats.Length-1; i--)
        {
            motionNormals[i] = Vector4.zero;
            points[i] = Vector4.zero;
        }

        for (int i = 0; i < sats.Length; i++)
        {
            Vector3 tmpPos = sats[i].transform.position;
            points[i] = new Vector4(tmpPos.x, tmpPos.y, tmpPos.z, 1);

            Vector3 motionVec = sats[i].transform.right;
            motionNormals[i] = new Vector4(motionVec.x, motionVec.y, motionVec.z, 1);

        }
        coneMaterial.SetVectorArray("_Points", points);
        coneMaterial.SetVectorArray("_OrbitNormals", motionNormals);
    }
}
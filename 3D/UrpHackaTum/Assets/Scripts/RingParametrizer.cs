
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RingParametrizer : MonoBehaviour
{
    public int numberOfSats;
    public float radius;
    // Start is called before the first frame update
    void OnValidate()
    {
        var components = transform.GetComponentsInChildren<SatelitesOnRing>();
        Debug.Log("setting " + components.Length);
        foreach(var comp in components)
        {
            comp.numberOfSats = numberOfSats;
            comp.radius = radius;
        }
    }

}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SatelitesOnRing : MonoBehaviour
{
    public bool refresh = false;
    public int numberOfSats;
    public float radius;
    public GameObject gameobject;


    float rotationRate;



    void OnValidate()
    {
        validation();
    }

    public void validation()
    {
        
        Vector3 point = transform.position;

        var destroyQueue = new Transform[transform.childCount];
        for (int i = 0; i < destroyQueue.Length; i++)
        {
            destroyQueue[i] = transform.GetChild(i);
        }



        #if UNITY_EDITOR
        UnityEditor.EditorApplication.delayCall += () =>
        {
            foreach (Transform child in destroyQueue)
            {
                DestroyImmediate(child.gameObject);
            }


        };
#endif

        transform.localScale = Vector3.one * radius;

        for (int i = 0; i < numberOfSats; i++)
        {
            /* Distance around the circle */
            var radians = 2 * Mathf.PI / (numberOfSats) * i;

            /* Get the vector direction */
            var vertical = Mathf.Sin(radians);
            var horizontal = Mathf.Cos(radians);

            var spawnDir = new Vector3(horizontal, 0, vertical);

            /* Get the spawn position */
            var spawnPos = point + spawnDir; // Radius is just the distance away from the point
            spawnPos = transform.localToWorldMatrix.MultiplyPoint(spawnPos);

            /* Now spawn */
            var enemy = Instantiate(gameobject, spawnPos, Quaternion.identity) as GameObject;

            /* Rotate the enemy to face towards player */
            enemy.transform.LookAt(point, -transform.up);
            enemy.transform.parent = transform;

        }

        float velocity = Mathf.Sqrt(Constants.M_earth * Constants.G / unityToM(radius));
        Debug.Log($"Sattellites are flying with a velocity of {velocity} m/s");

        rotationRate = velocity * 360f / (2 * Mathf.PI * unityToM(radius)); // 2PI / time = 2PI / (circumference / velocity)
        Debug.Log($"Resulting in a rotation period of {(2 * Mathf.PI * unityToM(radius))/ velocity/3600/24} days");
        
    }
    void Start()
    {
        
        //validation();
    }

    float unityToM(float unityValue)
    {
        return unityValue * 1e6f;
    }

    // Update is called once per frame
    void Update()
    {
        transform.RotateAround(transform.position, transform.up, EarthManager.timeScale * rotationRate * Time.deltaTime);
    }
}

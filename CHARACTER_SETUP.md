x# 🎭 **Character Setup Instructions**

## 🚀 **Quick Setup (5 minutes)**

### **Option 1: Download Ready Character**
1. **Visit Mixamo**: https://www.mixamo.com/
2. **Create free account** (Adobe ID)
3. **Browse Characters** → Select any character
4. **Download** → Format: FBX, Skin: With Skin
5. **Rename** to `character.glb` (we'll convert it)

### **Option 2: Use Free Blender Character**
1. **Download from Sketchfab**: https://sketchfab.com/3d-models?features=rigged&sort_by=-likeCount&type=downloadable
2. **Filter**: Rigged, Downloadable, Free
3. **Download** GLB format
4. **Place** in `frontend/public/models/character.glb`

---

## 🎨 **Blender Conversion (If needed)**

### **Convert FBX to GLB**
```blender
1. Open Blender
2. Delete default cube (X → Delete)
3. File → Import → FBX → Select your character
4. File → Export → glTF 2.0
   ✅ Selected Objects
   ✅ Include Animations
   ✅ Format: GLB (binary)
5. Save as: character.glb
```

---

## 📁 **File Structure**
```
frontend/
├── public/
│   └── models/
│       └── character.glb    ← Place your character here
├── src/
│   └── components/
│       ├── BlenderCharacter.tsx
│       └── SimpleSignAvatar.tsx
```

---

## 🎬 **Adding Custom Animations**

### **In Blender:**
```blender
1. Select armature → Pose Mode
2. Create keyframes for gestures:
   - Frame 1: Rest pose
   - Frame 30: Gesture peak
   - Frame 60: Return to rest
3. Name actions: "wave", "prayer", "thumbsUp", etc.
4. Export with animations
```

### **In Code:**
```javascript
// Update gestureAnimations in BlenderCharacter.tsx
const gestureAnimations = {
  'HELLO': 'wave',           // Your Blender action name
  'THANK_YOU': 'prayer',     // Your Blender action name
  'YES': 'thumbsUp',         // Your Blender action name
  // Add more mappings...
};
```

---

## 🔧 **Testing Your Character**

1. **Place character.glb** in `/public/models/`
2. **Start the app**: `npm run dev`
3. **Click 3D button** in the header
4. **Test gestures** → Character should animate
5. **Use mouse** to rotate and zoom the character

---

## 🎯 **Character Requirements**

### **Essential Features:**
- ✅ **Rigged skeleton** (armature with bones)
- ✅ **Hand bones** for finger animations
- ✅ **GLB format** (not FBX or OBJ)
- ✅ **Reasonable size** (< 10MB recommended)

### **Optional Features:**
- 🎭 **Facial bones** for expressions
- 🎨 **Textures** for realistic appearance
- 🎬 **Pre-made animations** for gestures
- 👕 **Clothing/accessories**

---

## 🐛 **Troubleshooting**

### **Character not loading?**
```bash
✅ Check file path: /public/models/character.glb
✅ Verify GLB format (not GLTF + separate files)
✅ Check file size (< 50MB)
✅ Look at browser console for errors
```

### **No animations?**
```bash
✅ Ensure animations exported from Blender
✅ Check action names match code
✅ Verify armature is included
```

### **Character too big/small?**
```javascript
// In BlenderCharacter.tsx, adjust:
scale={[2, 2, 2]}        // Make bigger
scale={[0.5, 0.5, 0.5]}  // Make smaller
```

---

## 🎨 **Recommended Characters**

### **Free Sources:**
1. **Mixamo**: Professional characters with animations
2. **Sketchfab**: Community creations
3. **Blender Cloud**: High-quality assets
4. **Ready Player Me**: Customizable avatars

### **Character Styles:**
- 👤 **Realistic Human**: For professional applications
- 🤖 **Stylized/Cartoon**: For friendly, approachable feel
- 🦸 **Fantasy/Sci-fi**: For creative applications
- 👶 **Simple/Low-poly**: For performance optimization

---

## 🚀 **Next Steps**

1. **Get a character** using Option 1 or 2 above
2. **Place in models folder**
3. **Test in SilentVoice**
4. **Customize animations** if needed
5. **Share your creation** with the community!

**Ready to bring your character to life?** Start with Mixamo for the easiest setup! 🎉
